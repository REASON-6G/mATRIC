import logging
import time
import json
from wiremq.gateway.endpoints import endpointfactory
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection setup
influxdb_url = 'http://localhost:8086'  # Replace with your InfluxDB server URL
token = 'your-token'  # Replace with your InfluxDB token
org = 'your-org'  # Replace with your organization name
bucket = 'your-bucket'  # Replace with your bucket name
client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

logger = logging.getLogger("channel1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["channel1_config"]

ch1 = endpointfactory.EndpointFactory().build(config)

while True:
    msgs = ch1.receive()
    for msg in msgs:
        logger.info(msg)

        # Parse the message
        msg_data = json.loads(msg)

        # Create a Point with the data
        point = Point("measurement_name").tag("matricID", msg_data.get('matricID', 'default')).field("data", msg_data)
        
        # Write the point to InfluxDB
        write_api.write(bucket=bucket, org=org, record=point)

    time.sleep(0.5)

# Close the InfluxDB client
client.close()
