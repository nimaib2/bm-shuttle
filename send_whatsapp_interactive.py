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
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + number,
                body="How many people are in your party? Select a number 0-3"
            )
            print(f"Text message sent: {message.sid}")
        except Exception as e:
            print(f"Failed to send message to {number}: {e}")

# Let's try the simple approach first
send_text_with_options()