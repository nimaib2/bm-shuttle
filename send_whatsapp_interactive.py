import os
from twilio.rest import Client

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

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
            body='How many people are in your party?:\n1. 0\n2. 1\n3. 2\n4. 3\n(Enter a number 1-4)'
    )
    print(f"Text message sent: {message.sid}")

# Let's try the simple approach first
send_text_with_options()