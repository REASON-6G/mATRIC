from influxdb_client import InfluxDBClient, Point, WriteOptions
import time

# InfluxDB settings
influxdb_url = 'http://localhost:8086'
token = 'your-token'
org = 'your-org'
bucket_5G = '5Gaccess'
bucket_wifi = 'WiFiaccess'

# Function to query data from InfluxDB
def query_influxdb(bucket_name):
    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
    query_api = client.query_api()

    query = f'from(bucket: "{bucket_name}") |> range(start: -1h)'
    result = query_api.query(org=org, query=query)

    for table in result:
        for record in table.records:
            print(f'Time: {record.get_time()}, Value: {record.get_value()}')

    client.close()

# Main loop to run the function every 10 seconds
while True:
    print("Querying 5Gaccess bucket...")
    query_influxdb(bucket_5G)

    print("Querying WiFiaccess bucket...")
    query_influxdb(bucket_wifi)

    time.sleep(10)