import logging
import time
import psutil
import json
from wiremq.gateway.endpoints import endpointfactory

"""
Pubsub 1 sends messages to 2 subscribers about CPU and RAM monitoring data.

Channel 2 is pre-subscribed to the pubsub on both topics with no criteria.

Channel 1 subscribes using a subscription command message and has criteria.
"""

logger = logging.getLogger("pubsub1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["pubsub1_config"]

def make_event_message_cpu():
    cpu_stats = psutil.cpu_stats()
    message =  {
        "type": "event",
        "payload": {
            "params": {
                "topic": "cpu",
                "cpu_percent": psutil.cpu_percent(),
                "ctx_switches": cpu_stats[0],
                "interrupts": cpu_stats[1],
                "soft_interrupts": cpu_stats[2],
                "syscalls": cpu_stats[3]
            }
        }
    }
    return message

def make_event_message_ram():
    mem = psutil.virtual_memory()
    message = {
        "type": "event",
        "payload": {
            "params": {
                "topic": "ram",
                "total": mem[0],
                "available": mem[1],
                "percent": mem[2],
                "used": mem[3],
                "free": mem[4],
                "active": mem[5],
                "inactive": mem[6],
                "buffers": mem[7],
                "cached": mem[8],
                "shared": mem[9],
                "slab": mem[10]
            }
        }
    }
    return message

ps1 = endpointfactory.EndpointFactory().build(config)

# Pre-subscribe Channel 2
subscription_config = {
    "sender_alias": "channel2",
    "payload": {
        "params": {
            "host": "127.0.0.1",
            "port": 8804,
            "topics": ["cpu", "ram"],
        }
    }
}
ps1.add_subscriber(subscription_config)

while True:
    logger.test("SENDING RAM NOTIFICATION")
    ps1.notify(make_event_message_ram())
    time.sleep(1)
    logger.test("SENDING CPU NOTIFICATION")
    ps1.notify(make_event_message_cpu())
    time.sleep(1)
    logger.test(ps1._subscribers)
