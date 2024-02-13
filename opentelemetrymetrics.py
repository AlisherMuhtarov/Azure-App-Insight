import os
import asyncio
import subprocess
import psutil 
import time
from typing import Iterable
from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter

exporter = AzureMonitorMetricExporter.from_connection_string(
    os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)

reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))
meter = metrics.get_meter_provider().get_meter("test-meters")

cpu_usage_metric = meter.create_up_down_counter(
    name="cpu_usage",
    description="CPU Usage",
    unit="percent",
)

def cpu_usage_retrieval(interval=1):

    while True:
        # Get cpu percantage
        cpu_usage = psutil.cpu_percent(interval=interval)
        print(f"CPU Usage: {cpu_usage}%")

        # Update the metrics
        cpu_usage_metric.add(-(cpu_usage))
        cpu_usage_metric.add(cpu_usage)

        time.sleep(interval)

cpu_usage_retrieval()

meter_provider.force_flush()
