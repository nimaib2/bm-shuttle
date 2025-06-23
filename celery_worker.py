from celery import Celery
from celery.schedules import crontab
from twilio.rest import Client
import os
from datetime import datetime, timezone, timedelta

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
celery = Celery('tasks', broker='redis://localhost:6379/0')
client = Client(account_sid, auth_token)

END_DATE = datetime(2025, 6, 30, tzinfo=timezone.utc)

@celery.task
def send_scheduled_messages():
    client.messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+14252463728',
        body="This is an automatic message sent through celery"
    )
    now = datetime.now(timezone.utc)
    if now > END_DATE:
        print("Task expired, not sending messages.")
        return

# Schedule the task to run 10 minutes from now
run_at = datetime.now(timezone.utc) + timedelta(minutes=3)
send_scheduled_messages.apply_async(eta=run_at)

celery.conf.beat_schedule={
    'send-messages-every-hour': {
        'task': 'celery_worker.send_scheduled_messages',
        'schedule': crontab(minute=5),
    },
}