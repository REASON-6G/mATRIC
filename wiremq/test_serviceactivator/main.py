import logging
import time
import json
from typing import Dict
from wiremq.gateway.endpoints import (
    serviceactivator,
    messagebus
)

logger = logging.getLogger("serviceactivator1_logger")

with open("config.json", "r") as f:
    config = json.load(f)
sa_config = config["serviceactivator1_config"]
bus0_config = config["bus0_config"]

def add_routing(message: Dict):
    service = message["payload"]["service"]
    if service == "cpu":
        dest_port = 9011
    elif service == "ram":
        dest_port = 9012
    message["dest_port"] = dest_port
    return message


sa = serviceactivator.ServiceActivator(sa_config)
bus = messagebus.MessageBus(bus0_config)

sa1 = sa.build()
sa1.start_server()
bus0 = bus.build()

while True:
    sa1.process()
    bus0.process()
    msgs = bus0.receive()
    for msg in msgs:
        logger.test(f"bus received: {msg}")
        # First, check if the received message is a response from one of the
        # other bus endpoints, we will know this if it has a transaction
        # correlation id
        if msg["tx_correlation_id"]:
            # Use the service activator to respond to the HTTP server
            logger.test("main sending response")
            logger.test(msg)
            sa1.send(msg)
            sa1.process()
        else:
            # The message has no transaction correlation id, therefore it is
            # a request from the serviceactivator
            logger.test("bus0 sending fresh")
            msg = add_routing(msg)
            bus0.send(msg)
    time.sleep(0.05)

bus0.close()
sa1.close()
