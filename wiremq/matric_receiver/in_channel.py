import logging
import time
import json
from wiremq.gateway.endpoints import endpointfactory

logger = logging.getLogger("in_channel_logger")

with open("config.json", "r") as f:
    config = json.load(f)["in_channel_config"]

ch1 = endpointfactory.EndpointFactory().build(config)
logger.test(f"Listening on {config['host']}:{config['port']}")

while True:
    msgs = ch1.receive()
    for msg in msgs:
        logger.test(json.dumps(msg, indent=2))
    time.sleep(0.05)
