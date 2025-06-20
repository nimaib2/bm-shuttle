import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

print("SID:", account_sid)
print("TOKEN:", auth_token)

numbers = [
    '+14252463728',
    '+14258948971',
]

# Method 3: Simple text message with instructions
def send_text_with_options():
    for number in numbers:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:' + number,
            content_sid='YOUR_APPROVED_LIST_TEMPLATE_SID',
            content_variables='{"1":"Option 1","2":"Option 2"}'
        )
        print(f"Text message sent: {message.sid}")

# Let's try the simple approach first
send_text_with_options()