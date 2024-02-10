import os
import asyncio
import subprocess
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter.from_connection_string(
    os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(exporter, schedule_delay_millis=60000)
trace.get_tracer_provider().add_span_processor(span_processor)

async def check_for_new_users(user_count):
    while True:

        new_user_added, user_count = check_users(user_count)

        if new_user_added:
            with tracer.start_as_current_span("user_added_event"):
                print("User added event sent!")
        else:
            print("No new users")

        await asyncio.sleep(60) 

def check_users(user_count):

    users_output = subprocess.check_output(['getent', 'passwd']).decode('utf-8')

    current_user_count = len(users_output.splitlines())

    new_user_added = current_user_count > user_count

    return new_user_added, current_user_count

if __name__ == "__main__":
    user_count = 34

    asyncio.run(check_for_new_users(user_count))
