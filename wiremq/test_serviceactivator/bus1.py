"""Bus1 responds to CPU related queries"""
import json
import uuid
import logging
import time
import psutil
from typing import Dict
from wiremq.gateway.endpoints import endpointfactory

logger = logging.getLogger("bus1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["bus1_config"]

def get_cpu_data(command: str):
    if command == "get_percent":
        return psutil.cpu_percent()
    elif command == "get_temperatures":
        return psutil.sensors_temperatures()


def compose_response(message: Dict):
    data = get_cpu_data(message["payload"]["command"])
    return {
        "type": message["type"],
        "correlation_id": message["message_id"],
        "tx_id": str(uuid.uuid4()),
        "tx_correlation_id": message["tx_id"],
        "error_code": 200,
        "error_message": "OK",
        "dest_ip": "127.0.0.1",
        "dest_port": 9010,
        "payload": {
            "data": data
        }
    }


bus1 = endpointfactory.EndpointFactory().build(config)
while True:
    msgs = bus1.receive()
    for msg in msgs:
        logger.test(f"received request: {msg['payload']['command']}")
        logger.test(msg)
        response = compose_response(msg)
        bus1.send(response)
    time.sleep(0.05)
