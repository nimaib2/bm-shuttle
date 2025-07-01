# 1. --- Verify your current Azure CLI login and subscription context ---
#    Ensure you are logged into the Azure account that contains the subscription
#    where you want to deploy your resources (ACR, ACI).
echo "Verifying current Azure CLI account context:"
az account show --query "{SubscriptionId:id, TenantId:tenantId, Name:name, IsDefault:isDefault}" --output json
echo "--------------------------------------------------------"

# Copy these values into your GitHub Secrets immediately:
# AZURE_SUBSCRIPTION_ID: (from SubscriptionId in output)
# AZURE_TENANT_ID: (from TenantId in output)

# Set variables based on your environment
AZURE_SUBSCRIPTION_ID="5e54670a-77cf-4fe3-b1d3-4183de67491c"
AZURE_RESOURCE_GROUP="Shuttle" # e.g., myflaskapp-rg (the RG where your ACR/ACI will live)
AZURE_APP_NAME="github-actions-myflaskapp" # The display name for your AAD app. Keep this consistent.

# Your GitHub username/organization and repository name
YOUR_GITHUB_OWNER="nimaib2" # Your GitHub username if not an organization
YOUR_REPO_NAME="bm-shuttle"
GITHUB_ENVIRONMENT_NAME="production" # Must match 'environment: production' in your workflow YAML

echo "Using Subscription ID: $AZURE_SUBSCRIPTION_ID"
echo "Using Resource Group: $AZURE_RESOURCE_GROUP"
echo "Azure AD App Name: $AZURE_APP_NAME"
echo "GitHub Repo Owner: $YOUR_GITHUB_OWNER"
echo "GitHub Repo Name: $YOUR_REPO_NAME"
echo "GitHub Environment: $GITHUB_ENVIRONMENT_NAME"
echo "--------------------------------------------------------"

# 2. --- Create Azure AD Application ---
#    This command creates the application and captures its client ID (appId).
echo "Creating Azure AD Application..."
AZURE_APP_ID=$(az ad app create \
  --display-name "$AZURE_APP_NAME" \
  --query appId --output tsv)
echo "Azure AD Application (Client) ID (AZURE_CLIENT_ID): $AZURE_APP_ID"
echo "--------------------------------------------------------"

# Copy this AZURE_APP_ID into your GitHub Secret:
# AZURE_CLIENT_ID: (the value printed above)

# 3. --- Create Service Principal for the Application ---
#    This command creates the Service Principal and captures its object ID (spId).
echo "Creating Service Principal..."
AZURE_SP_ID=$(az ad sp create --id $AZURE_APP_ID --query id --output tsv)
echo "Service Principal Object ID (AZURE_SP_ID): $AZURE_SP_ID"
echo "--------------------------------------------------------"

# 4. --- Assign Permissions (Contributor role) to the Service Principal ---
#    This grants the SP access to your resource group/subscription.
echo "Assigning Contributor role to Service Principal on resource group: $AZURE_RESOURCE_GROUP"
az role assignment create \
  --role contributor \
  --scope "/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$AZURE_RESOURCE_GROUP" \
  --assignee $AZURE_SP_ID
echo "Role assignment created."
echo "--------------------------------------------------------"

# 5. --- Create the Federated Credential ---
#    This links your GitHub repo/environment to the Azure AD app.
echo "Creating federated credential..."
az ad app federated-credential create \
  --id $AZURE_APP_ID \
  --parameters '{
    "name": "GitHubActions",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'$YOUR_GITHUB_OWNER'/'$YOUR_REPO_NAME':environment:'$GITHUB_ENVIRONMENT_NAME'",
    "audiences": ["api://AzureADTokenExchange"]
  }'
echo "Federated credential created."
echo "--------------------------------------------------------"

echo "ALL SETUP COMMANDS EXECUTED. PLEASE UPDATE GITHUB SECRETS WITH THE PRINTED VALUES."
echo "AZURE_CLIENT_ID: $AZURE_APP_ID"
echo "AZURE_TENANT_ID: (from 'az account show' output)"
echo "AZURE_SUBSCRIPTION_ID: (from 'az account show' output)"
echo "ACR_NAME: <your-acr-name>" # Add this if not already in secrets
echo "AZURE_RESOURCE_GROUP: $AZURE_RESOURCE_GROUP" # Add this if not already in secrets
echo "--------------------------------------------------------"