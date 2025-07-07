from dotenv import load_dotenv
from flask import Flask, request
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client as SupabaseClient
from datetime import datetime, timezone, timedelta
from flask_apscheduler import APScheduler
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

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

END_DATE = datetime(2026, 6, 30, tzinfo=timezone.utc)

# Configure Resource (optional, but good practice)
resource = Resource.create({"service.name": "badge-mane-webhook"})

# Configure TracerProvider
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Configure Exporter to use Azure Monitor exporter
# It will automatically pick up APPLICATIONINSIGHTS_CONNECTION_STRING from env
connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if connection_string:
    print(f"Configuring Azure Monitor with connection string: {connection_string[:50]}...")
    
    try:
        # Use the simpler exporter approach for faster startup
        azure_exporter = AzureMonitorTraceExporter(connection_string=connection_string)
        span_processor = BatchSpanProcessor(azure_exporter)
        provider.add_span_processor(span_processor)
        print("Azure Monitor OpenTelemetry exporter configured successfully")
        
        # Custom Live Metrics implementation (simpler and faster)
        def send_live_metrics():
            """Send periodic live metrics to Application Insights"""
            try:
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span("live_metrics_heartbeat") as span:
                    import psutil
                    
                    # Get system metrics
                    cpu_percent = psutil.cpu_percent()
                    memory = psutil.virtual_memory()
                    
                    # Add live metrics attributes
                    span.set_attribute("live_metrics.cpu_percent", cpu_percent)
                    span.set_attribute("live_metrics.memory_percent", memory.percent)
                    span.set_attribute("live_metrics.memory_available_mb", memory.available / 1024 / 1024)
                    span.set_attribute("live_metrics.timestamp", datetime.now(timezone.utc).isoformat())
                    span.set_attribute("live_metrics.service_status", "running")
                    
                    print(f"Live metrics sent - CPU: {cpu_percent}%, Memory: {memory.percent}%")
            except Exception as e:
                print(f"Live metrics error: {e}")
        
        # Schedule live metrics every 60 seconds (less frequent to reduce load)
        scheduler.add_job(
            id='live_metrics_job',
            func=send_live_metrics,
            trigger='interval',
            seconds=60,
            max_instances=1  # Prevent overlapping executions
        )
        print("Live Metrics scheduled to run every 60 seconds")
        
    except Exception as e:
        print(f"OpenTelemetry setup failed: {e}")
        print("Continuing without telemetry...")
        
else:
    print("Warning: APPLICATIONINSIGHTS_CONNECTION_STRING not found. Telemetry will not be sent to Azure Monitor.")

# Instrument Flask and Requests
FlaskInstrumentor().instrument_app(app) # 'app' is your Flask app instance
RequestsInstrumentor().instrument() # Instrument the 'requests' library

def send_scheduled_message():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("send_scheduled_message") as span:
        print(f"send_scheduled_message called at {datetime.now()}")
        span.set_attribute("function.name", "send_scheduled_message")
        span.set_attribute("service.name", "badge-mane-webhook")
        
        now = datetime.now(timezone.utc)
        span.set_attribute("execution.timestamp", now.isoformat())
        
        if now > END_DATE:
            print("Task expired, not sending messages.")
            span.set_attribute("task.status", "expired")
            span.set_attribute("task.end_date", END_DATE.isoformat())
            return
        
        try:
            print("Attempting to send message...")
            span.set_attribute("message.attempt", True)
            span.set_attribute("twilio.from_number", "+14155238886")
            span.set_attribute("twilio.to_number", "+14252463728")
            
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:+14252463728',
                body="Hello, this is a test message from Twilio."
            )
            print(f"Message sent successfully! SID: {message.sid}")
            print(f"Message status: {message.status}")
            
            span.set_attribute("message.sid", message.sid)
            span.set_attribute("message.status", message.status)
            span.set_attribute("task.status", "success")
            
        except Exception as e:
            print(f"Error sending message: {e}")
            span.set_attribute("task.status", "error")
            span.set_attribute("error.message", str(e))
            span.record_exception(e)
            raise

# Schedule a one-off job (runs 3 minutes from now)
try:
    run_time = datetime.now() + timedelta(minutes=3)
    scheduler.add_job(
        id='one_time_job',
        func=send_scheduled_message,
        trigger='date',
        run_date=run_time,
        max_instances=1
    )
    # scheduler.remove_job('one_time_job')  # Commented out so the job can actually run
    print('One-time job scheduled for:', run_time)
except Exception as e:
    print(f"Failed to schedule one-time job: {e}")

# Schedule a recurring job (every hour at minute 5)
try:
    scheduler.add_job(
        id='hourly_job',
        func=send_scheduled_message,
        trigger='cron',
        minute=5,
        max_instances=1
    )
    print("Hourly job scheduled successfully")
except Exception as e:
    print(f"Failed to schedule hourly job: {e}")

# Add a test job that runs every 5 minutes for testing (remove this in production)
try:
    scheduler.add_job(
        id='test_job_every_5_min',
        func=send_scheduled_message,
        trigger='cron',
        minute='*/5',  # Every 5 minutes
        max_instances=1
    )
    print('Test job scheduled to run every 5 minutes')
except Exception as e:
    print(f"Failed to schedule test job: {e}")

# Clean up expired jobs
try:
    if datetime.now(timezone.utc) > END_DATE:
        if scheduler.get_job('hourly_job'):
            scheduler.remove_job('hourly_job')
        if scheduler.get_job('test_job_every_5_min'):
            scheduler.remove_job('test_job_every_5_min')
        print("Expired jobs removed")
except Exception as e:
    print(f"Error cleaning up jobs: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("webhook_request") as span:
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        # Check for context.messageId for replies to interactive messages
        replied_message_id = request.values.get('context.messageId', None)

        # Add telemetry attributes
        span.set_attribute("webhook.message_body", incoming_msg)
        span.set_attribute("webhook.from_number", from_number)
        span.set_attribute("webhook.method", request.method)
        if replied_message_id:
            span.set_attribute("webhook.replied_message_id", replied_message_id)

        print(f"Received message: '{incoming_msg}' from {from_number}")
        if replied_message_id:
            print(f"Message replied to: {replied_message_id}")

        resp = MessagingResponse()

        # Main menu
        if incoming_msg in ['menu', 'hi', 'hello', 'start', 'main']:
            span.set_attribute("webhook.response_type", "main_menu")
            msg = resp.message(
                "How many people are in your party?:\n1. 0\n2. 1\n3. 2\n4. 3\n(Enter a number 1-4)"
            )
        elif incoming_msg in ['1', '2', '3', '4']:
            span.set_attribute("webhook.response_type", "party_size_selection")
            span.set_attribute("webhook.selected_party_size", int(incoming_msg)-1)
            # Only insert if it's a valid number
            # data = {
            #     "created_at": datetime.now(timezone.utc).isoformat(),
            #     "phone_number": str(from_number[len("whatsapp:"):]),
            #     "response": int(incoming_msg)
            # }
            # supabase.table("MessageInfo").insert(data).execute()
            # print('data sent to supabase')
            msg = resp.message(f"You selected {int(incoming_msg)-1} people. Thank you! If you want to start over, reply 'menu'.")
        else:
            span.set_attribute("webhook.response_type", "unrecognized_input")
            msg = resp.message("Sorry, I didn't understand that. Please reply with a number 1-4, or 'menu' to see options.")

        span.set_attribute("webhook.response_sent", True)
        return str(resp)

@app.route('/health', methods=['GET'])
def health():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("health_check") as span:
        import psutil
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        
        # Add metrics to telemetry
        span.set_attribute("system.cpu_percent", cpu_percent)
        span.set_attribute("system.memory_percent", memory.percent)
        span.set_attribute("system.memory_available_mb", memory.available / 1024 / 1024)
        span.set_attribute("health.status", "healthy")
        
        health_data = {
            "status": "healthy", 
            "message": "Webhook server is running",
            "metrics": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": round(memory.available / 1024 / 1024, 2)
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return health_data

@app.route('/test-message', methods=['GET'])
def test_message():
    try:
        print("Manual test message triggered")
        send_scheduled_message()
        return {"status": "success", "message": "Test message sent"}
    except Exception as e:
        print(f"Test message failed: {e}")
        return {"status": "error", "message": str(e)}

@app.route('/live-metrics', methods=['GET'])
def live_metrics():
    """Endpoint that provides live metrics data similar to Application Insights Live Metrics"""
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("live_metrics_endpoint") as span:
        import psutil
        
        # Get comprehensive system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get process-specific metrics
        process = psutil.Process()
        process_memory = process.memory_info()
        
        metrics_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "server_health": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": round(memory.available / 1024 / 1024, 2),
                "memory_used_mb": round(memory.used / 1024 / 1024, 2),
                "disk_percent": round((disk.used / disk.total) * 100, 2),
                "disk_free_gb": round(disk.free / 1024 / 1024 / 1024, 2)
            },
            "process_health": {
                "memory_rss_mb": round(process_memory.rss / 1024 / 1024, 2),
                "memory_vms_mb": round(process_memory.vms / 1024 / 1024, 2),
                "threads": process.num_threads(),
                "cpu_percent": process.cpu_percent()
            },
            "application_status": {
                "status": "healthy",
                "uptime_seconds": (datetime.now() - datetime.fromtimestamp(process.create_time())).total_seconds(),
                "scheduler_jobs": len(scheduler.get_jobs())
            }
        }
        
        # Add telemetry attributes
        for category, data in metrics_data.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    span.set_attribute(f"live_metrics.{category}.{key}", value)
        
        return metrics_data

if __name__ == '__main__':
    print("Starting webhook server...")
    app.run(debug=True, port=5000, host='0.0.0.0')