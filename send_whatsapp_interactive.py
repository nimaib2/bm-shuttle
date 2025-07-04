import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

# print("SID:", account_sid)
# print("TOKEN:", auth_token)

numbers = [
    '+14252463728',
    '+14258948971',
]

# Method 3: Simple text message with instructions
def send_text_with_options():
    for number in numbers:
        try:
            client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:+14252463728',
                content_sid='HXae9b8723945109e491519a77de8d46d3'
            )
        except Exception as e:
            print(f"Failed to send message to {number}: {e}")

# Let's try the simple approach first
send_text_with_options()