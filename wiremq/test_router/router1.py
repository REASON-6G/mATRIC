import logging
import time
import json
from wiremq.gateway.endpoints import endpointfactory

logger = logging.getLogger("router1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["router1_config"]

rt1 = endpointfactory.EndpointFactory().build(config)
while True:
    rt1.process()
    time.sleep(0.01)
