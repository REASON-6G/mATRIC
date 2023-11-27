import logging
import time
import json
from wiremq.gateway.endpoints import endpointfactory
from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('localhost', 27017)  # Replace with your MongoDB server details
db = client['your_database_name']  # Replace with your database name

logger = logging.getLogger("channel1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["channel1_config"]

ch1 = endpointfactory.EndpointFactory().build(config)

while True:
    msgs = ch1.receive()
    for msg in msgs:
        logger.info(msg)  # Changed from logger.test to logger.info

        # Parse the message and extract matricID
        msg_data = json.loads(msg)
        matricID = msg_data.get('matricID', 'default_collection')  # Use a default collection if matricID is missing

        # Get or create the collection with the name of matricID
        collection = db[matricID]

        # Insert the message into the collection
        collection.insert_one(msg_data)

    time.sleep(0.5)