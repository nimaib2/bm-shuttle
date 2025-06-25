from dotenv import load_dotenv
from flask import Flask, request
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client as SupabaseClient
from datetime import datetime, timezone, timedelta
from flask_apscheduler import APScheduler

load_dotenv()
# print("SUPABASE_URL:", os.getenv('SUPABASE_URL'))
# print("SUPABASE_KEY:", os.getenv('SUPABASE_KEY'))
app = Flask(__name__)

# Initialize APScheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
# gets supabase key and url from .env or sets to an empty string otherwise
supabase_url: str=os.getenv('SUPABASE_URL') or ""
supabase_key: str=os.getenv('SUPABASE_KEY') or ""
client = Client(account_sid, auth_token)
supabase: SupabaseClient = create_client(supabase_url, supabase_key)

END_DATE = datetime(2025, 6, 30, tzinfo=timezone.utc)

def send_scheduled_message():
    now = datetime.now(timezone.utc)
    if now > END_DATE:
        print("Task expired, not sending messages.")
        return
    client.messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+14252463728',
        body="This is an automatic message sent through APScheduler"
    )

# Schedule a one-off job (runs 3 minutes from now)
run_time = datetime.now() + timedelta(minutes=3)
scheduler.add_job(
    id='one_time_job',
    func=send_scheduled_message,
    trigger='date',
    run_date=run_time
)
scheduler.remove_job('one_time_job')
print('job removed')

# Schedule a recurring job (every hour at minute 5)
scheduler.add_job(
    id='hourly_job',
    func=send_scheduled_message,
    trigger='cron',
    minute=5
)

if datetime.now(timezone.utc)>END_DATE:
    scheduler.remove_job('hourly_job')

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
    elif incoming_msg in ['1', '2', '3', '4']:
        # Only insert if it's a valid number
        data = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "phone_number": str(from_number[len("whatsapp:"):]),
            "response": int(incoming_msg)
        }
        supabase.table("MessageInfo").insert(data).execute()
        msg = resp.message(f"You selected {int(incoming_msg)-1} people. Thank you! If you want to start over, reply 'menu'.")
    else:
        msg = resp.message("Sorry, I didn't understand that. Please reply with a number 1-4, or 'menu' to see options.")

    return str(resp)

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy", "message": "Webhook server is running"}

if __name__ == '__main__':
    print("Starting webhook server...")
    app.run(debug=True, port=5000, host='0.0.0.0')