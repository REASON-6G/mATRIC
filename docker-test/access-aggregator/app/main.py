import logging
import time
import json
from pathlib import Path
import os
from wiremq.gateway.endpoints import endpointfactory

logger = logging.getLogger("in_channel_logger")

path = Path(__file__).parent
config_path = os.path.join(path, "config.json")
with open(config_path, "r") as f:
    config = json.load(f)["in_channel_config"]

ch1 = endpointfactory.EndpointFactory().build(config)
logger.test(f"Listening on {config['host']}:{config['port']}")

# TODo write a function that receives the msg, deconstructs it to understand what is the AP tech and then pushes to the appropriate bucket

while True:
    msgs = ch1.receive()
    for msg in msgs:
        logger.test(json.dumps(msg, indent=2))
    time.sleep(0.05)
