from dotenv import load_dotenv
from flask import Flask, request
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client as SupabaseClient

load_dotenv()
print("SUPABASE_URL:", os.getenv('SUPABASE_URL'))
print("SUPABASE_KEY:", os.getenv('SUPABASE_KEY'))
app = Flask(__name__)

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
# gets supabase key and url from .env or sets to an empty string otherwise
supabase_url: str=os.getenv('SUPABASE_URL') or ""
supabase_key: str=os.getenv('SUPABASE_KEY') or ""
client = Client(account_sid, auth_token)
supabase: SupabaseClient = create_client(supabase_url, supabase_key)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    print(f"Received message: '{incoming_msg}' from {from_number}")

    resp = MessagingResponse()

    # Main menu
    if incoming_msg in ['menu', 'hi', 'hello', 'start', 'main']:
        msg = resp.message(
            "How many people are in your party?:\n1. 0\n2. 1\n3. 2\n4. 3\n(Enter a number 1-4)"
        )
    elif incoming_msg in ['0']:
        msg = resp.message("You selected 0 people. Thank you! If you want to start over, reply 'menu'.")
    elif incoming_msg in ['1']:
        msg = resp.message("You selected 1 people. Thank you! If you want to start over, reply 'menu'.")
    elif incoming_msg in ['2']:
        msg = resp.message("You selected 2 people. Thank you! If you want to start over, reply 'menu'.")
    elif incoming_msg in ['3']:
        msg = resp.message("You selected 3 people. Thank you! If you want to start over, reply 'menu'.")
    else:
        msg = resp.message("Sorry, I didn't understand that. Please reply with a number 1-4, or 'menu' to see options.")

    return str(resp)

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy", "message": "Webhook server is running"}

if __name__ == '__main__':
    print("Starting webhook server...")
    app.run(debug=True, port=5000, host='0.0.0.0')