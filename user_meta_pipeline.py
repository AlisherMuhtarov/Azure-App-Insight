import os 
import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
exporter = AzureMonitorTraceExporter.from_connection_string(
    os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter, schedule_delay_millis=60000))


user = os.environ.get("USER")
user_id = os.environ.get("USER_ID")
build_result = os.environ.get("BUILD_RESULT", "false")

tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("user_meta") as span:
    span.set_attribute("user", user)
    span.set_attribute("user_id", user_id)
    span.set_attribute("user_status", build_result)

print(f"Build result: {build_result}")
