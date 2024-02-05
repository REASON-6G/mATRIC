import logging
import time
import json
from influxdb_client import InfluxDBClient, Point, WriteOptions
from pathlib import Path
import os
from wiremq.gateway.endpoints import endpointfactory

# InfluxDB settings (update with your actual settings)
# influxdb_url = 'http://10.128.2.174:8086'  # for remote connections
influxdb_url = "http://influxdb:8086"  # for local connections
token = 'XAyfr1nVMvW0eStmjIbJJzDIaC0rPt40wZiIlqy8yoauVp5V1mb_ZT1gLJX3ujrKJl64RZvsV4teq3iyw2UFfQ=='
org = 'UoB'
bucket_mapping = {
    '5G': '5G',
    'wifi': 'Wifi',
    'lifi': 'Lifi'
}

logger = logging.getLogger("in_channel_logger")

path = Path(__file__).parent
config_path = os.path.join(path, "config.json")
with open(config_path, "r") as f:
    config = json.load(f)["in_channel_config"]

client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# TODo write a function that receives the msg, deconstructs it to understand what is the AP tech and then pushes to the appropriate bucket
def write_to_influx(json_data):
#    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
#    write_api = client.write_api(write_options=WriteOptions(batch_size=1))

    # Parse and flatten the JSON data
    if isinstance(json_data, dict):
        data = json_data
    else:
        data = json.loads(json_data)
    flat_data = flatten_json(data)

    # Extract the 'Aptech' or 'APtech' field to determine the bucket
    aptech = flat_data.get('payload_data_Aptech') or flat_data.get('payload_data_APtech')

    if aptech and aptech in bucket_mapping:
        bucket = bucket_mapping[aptech]
        point = Point("measurement").tag("Aptech", aptech)
        if aptech == "wifi" or aptech == "lifi":
            mac_address = flat_data.get('payload_data_mac_address')
            point.tag("mac_address", mac_address)
        
        # Add each flattened field as a field in the Point
        for key, value in flat_data.items():
            point = point.field(key, value)

        # Write the point to InfluxDB
        logger.test(f"Writing to bucket: {bucket}")
        write_api.write(bucket=bucket, org=org, record=point)
        logger.test(f"Data written to bucket: {bucket}")
    else:
        logger.test("Invalid or missing Aptech/APtech field")

    client.close()


if __name__ == "__main__":
    ch1 = endpointfactory.EndpointFactory().build(config)
    logger.test(f"WireMQ Channel listening on port {config['port']}")

    while True:
        msgs = ch1.receive()
        for msg in msgs:
            logger.test(f"WireMQ Channel received {msg.get('message_id')} from"
                        f" {msg.get('sender_alias')}, payload = "
                        f"{json.dumps(msg.get('payload'))[:200]}...")
            write_to_influx(msg)
        time.sleep(0.05)
