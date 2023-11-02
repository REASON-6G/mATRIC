"""Bus1 responds to CPU related queries"""
import json
import uuid
import logging
import time
import psutil
from typing import Dict
from wiremq.gateway.endpoints import messagebus

logger = logging.getLogger("bus2_logger")

with open("config.json", "r") as f:
    config = json.load(f)["bus2_config"]


bus = messagebus.MessageBus(config)


def get_ram_data(command: str):
    mem = psutil.virtual_memory()
    if command == "get_percent":
        return mem[2]
    elif command == "get_total":
        return mem[0]
    elif command == "get_available":
        return mem[1]
    elif command == "get_free":
        return mem[4]


def compose_response(message: Dict):
    data = get_ram_data(message["payload"]["command"])
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


bus1 = bus.build()
while True:
    bus1.process()
    msgs = bus1.receive()
    for msg in msgs:
        logger.test(f"received request: {msg['payload']['command']}")
        response = compose_response(msg)
        bus1.send(response)
    time.sleep(0.05)
