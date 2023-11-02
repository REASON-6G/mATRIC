import logging
import time
import json
from wiremq.gateway.routers import router

logger = logging.getLogger("router1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["router1_config"]

rt = router.Router(config)

rt1 = rt.build()
while True:
    rt1.process()
    time.sleep(0.01)
