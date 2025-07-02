#!/bin/bash

# This script automates the process of setting up the Azure AD Federated Credential for GitHub Actions.
# It will:
# 1. Prompt for your Azure AD Application (Client) ID.
# 2. List and delete any existing federated credentials for that Application ID.
# 3. Create a new federated credential with the exact subject required by GitHub Actions.

echo "Azure AD Federated Credential Setup Script for GitHub Actions"
echo "------------------------------------------------------------"

# --- 1. Get Azure AD Application (Client) ID ---
echo ""
echo "Please enter your Azure AD Application (Client) ID."
echo "This is the 'AZURE_CLIENT_ID' you have in your GitHub Secrets."
echo "Example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
read -p "Enter Azure AD Application (Client) ID: " AZURE_APP_ID

if [ -z "$AZURE_APP_ID" ]; then
  echo "Error: Azure AD Application ID cannot be empty. Exiting."
  exit 1
fi

echo ""
echo "Verifying Azure CLI login..."
# Ensure you are logged into Azure CLI with the correct subscription
az account show > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "You are not logged into Azure CLI. Please log in first:"
  echo "az login"
  exit 1
fi
echo "Azure CLI login confirmed."

# --- 2. Delete Existing Federated Credentials ---
echo ""
echo "Attempting to list and delete any existing federated credentials for Application ID: $AZURE_APP_ID"
echo "This is crucial to ensure a clean state and avoid conflicts."

# Get IDs of all existing federated credentials for this app
FEDERATED_CREDENTIAL_IDS=$(az ad app federated-credential list --id "$AZURE_APP_ID" --query "[].id" --output tsv 2>/dev/null)

if [ -z "$FEDERATED_CREDENTIAL_IDS" ]; then
  echo "No existing federated credentials found. Proceeding to create a new one."
else
  echo "Found existing federated credentials. Deleting them now:"
  for FC_ID in $FEDERATED_CREDENTIAL_IDS; do
    echo "  - Deleting federated credential with ID: $FC_ID"
    az ad app federated-credential delete --id "$AZURE_APP_ID" --federated-credential-id "$FC_ID" --output none
    if [ $? -ne 0 ]; then
      echo "    Warning: Failed to delete federated credential $FC_ID. Please check permissions or delete manually in Azure Portal."
    fi
  done
  echo "Finished attempting to delete existing federated credentials."
  echo "Please wait 2-3 minutes for Azure AD changes to propagate before proceeding to the next step or re-running."
  read -p "Press Enter to continue after waiting (or Ctrl+C to exit): "
fi

# --- 3. Create the NEW, Correct Federated Credential ---
echo ""
echo "Creating the new federated credential with the precise subject required by GitHub Actions."

# These variables MUST exactly match what GitHub is sending in the OIDC token from your workflow logs
# Confirmed subject: 'repo:nimaib2/bm-shuttle:environment:production'
YOUR_GITHUB_OWNER="nimaib2"
YOUR_REPO_NAME="bm-shuttle" # THIS IS 'bm-shuttle', NOT 'badgemane-shuttle'
GITHUB_ENVIRONMENT_NAME="production"

echo "Using GitHub details: Owner=$YOUR_GITHUB_OWNER, Repo=$YOUR_REPO_NAME, Environment=$GITHUB_ENVIRONMENT_NAME"
echo "The subject will be: repo:$YOUR_GITHUB_OWNER/$YOUR_REPO_NAME:environment:$GITHUB_ENVIRONMENT_NAME"

az ad app federated-credential create \
  --id "$AZURE_APP_ID" \
  --parameters '{
    "name": "GitHubActions",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'"$YOUR_GITHUB_OWNER"'/'"$YOUR_REPO_NAME"':environment:'"$GITHUB_ENVIRONMENT_NAME"'",
    "audiences": ["api://AzureADTokenExchange"]
  }'

if [ $? -eq 0 ]; then
  echo ""
  echo "SUCCESS: Federated credential 'GitHubActions' created/updated successfully!"
  echo "Subject used: repo:$YOUR_GITHUB_OWNER/$YOUR_REPO_NAME:environment:$GITHUB_ENVIRONMENT_NAME"
  echo ""
  echo "NEXT STEPS:"
  echo "1. Ensure 'APPLICATIONINSIGHTS_CONNECTION_STRING' is set as a secret in GitHub if you haven't already."
  echo "2. Double-check your '.github/workflows/deploy_to_azure.yaml' to ensure the 'az container create' command"
  echo "   has the correct '--environment-variables' block and uses 'steps.azure-login.outputs.access_token'"
  echo "   for --registry-password."
  echo "3. Make a trivial commit (e.g., add a space to README.md) and push to your 'main' branch to trigger a new GitHub Actions workflow run."
  echo "4. Monitor the GitHub Actions run for success."
else
  echo ""
  echo "ERROR: Failed to create or update the federated credential."
  echo "Please review the error messages above and ensure:"
  echo "  - Your Azure AD Application ID is correct."
  echo "  - You have the necessary permissions in Azure AD."
  echo "  - The 'subject' string is precisely correct as expected by GitHub Actions."
fi

echo ""
echo "Script finished." 