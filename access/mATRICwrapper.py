# this code will generate 5G Nokia CLI data in json format
# the pubAPdata function should publish to wiremq the json object
# we need to implement the same generation for wifi and lifi
import os
import json
import random
import string
from datetime import datetime
from wiremq.gateway.endpoints import channel
from typing import (
    Dict,
    LiteralString
)

# Define the path to your JSON structure file
json_structure_file = './Nokia.json'
wmq_channel_config_file = './wmq-channel.json'

# Function to generate random time strings for the actualStartTime and actualStopTime
def generate_random_time():
    """Generate a random time string in the format of 'YYYY-MM-DDTHH:MM:SSZ'."""
    year = random.randint(2020, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # to avoid issues with February
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

# Function to generate a unique identifier for matricID
def generate_matric_id():
    """Generate a random matricID string."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# APManager class definition
class APManager:
    def __init__(self, structure_file_path, channel_file_path):
        self._channel = None
        # Read the JSON structure from the file
        if os.path.exists(structure_file_path):
            with open(structure_file_path, 'r') as file:
                self.json_5g_structure = json.load(file)
        else:
            raise FileNotFoundError(f"The structure file {structure_file_path} does not exist.")

        # Initialise the wiremq channel
        self._initialise_channel(channel_file_path)

    def _initialise_channel(self, channel_file_path: LiteralString) -> None:
        """Initialises a wiremq channel.

        This channel is used for outbound communication to another channel, on
        a P2P basis.

        Parameters
        ----------
        channel_file_path: str
            Directory path to the channel's configuration JSON file.
        """
        with open(channel_file_path, "rb") as f:
            channel_config = json.load(f)

        channel_builder = channel.Channel(channel_config)
        self._channel = channel_builder.build()

    def getAPdata(self, ap_type):
        """Generates a JSON object with a timestamp and matricID based on the AP type."""
        if ap_type.lower() == '5g':
            # Populate the 5G structure with random data
            data = self.populate_5g_data()
        elif ap_type.lower() in ['wifi', 'lifi']:
            # For now, return an empty structure for Wi-Fi and Li-Fi
            data = {}
        else:
            raise ValueError("AP type must be '5g', 'wifi', or 'lifi'.")
        
        # Add the current timestamp and matricID to the data
        data['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data['matricID'] = generate_matric_id()
        
        return data

    def populate_5g_data(self):
        """Populates the 5G JSON structure with random data."""
        data = json.loads(json.dumps(self.json_5g_structure))
        
        # Populate the JSON structure with random data
        data["distName"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["cellId"] = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        data["cellType"] = random.randint(1, 4)
        data["results"]["actualStartTime"] = generate_random_time()
        data["results"]["actualStopTime"] = generate_random_time()
        data["results"]["fwdTestDisp"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["result"] += ''.join(random.choices(string.ascii_letters, k=3))
        
        # Populate the rfAntResults with random data
        rf_ant_results = data["results"]["rfAntResults"]
        rf_ant_results["antId"] = random.randint(1, 10)
        rf_ant_results["fwdETPw"] = random.uniform(0, 100)
        rf_ant_results["fwdETPdBm"] = random.uniform(-100, 0)
        rf_ant_results["fwdTPEerror"] = random.uniform(0, 10)  # Assuming LTE only
        rf_ant_results["fwdTTPw"] = random.uniform(0, 100)     # Assuming LTE only
        rf_ant_results["fwdTTPdBm"] = random.uniform(-100, 0)  # Assuming LTE only
        rf_ant_results["rModId"] = random.randint(1, 100)
        rf_ant_results["rtwp"] = random.uniform(-100, 0)
        rf_ant_results["vswr"] = random.uniform(1, 3)
        rf_ant_results["rsi"] = random.uniform(-100, 0)        # Assuming NR only
        rf_ant_results["sinr"] = random.uniform(0, 30)         # Assuming NR only
        
        # Populate the rest of the fields with random data
        data["results"]["rvrsTestDisp"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["testOutcome"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["testOutcomeAdditionalInfo"] += ''.join(random.choices(string.ascii_letters, k=10))
        data["results"]["sinr"] = random.uniform(0, 30)        # Assuming LTE only

        return data

    def _construct_message(self, payload: Dict) -> Dict:
        """Builds headers and payload for a wiremq message.

        Parameters
        ----------
        payload: Dict
            The payload data from mATRIC access point.

        Returns
        -------
        message: Dict
            The constructed wiremq message.
        """
        message = {
            "type": "event",
            "payload": {
                "data": payload
            }
        }
        return message

    def pubAPdata(self, payload: Dict) -> None:
        """Publishes the access point data.

        Constructs a wiremq message and uses the wiremq channel to send data to
        another channel.

        Parameters
        ----------
        payload: Dict
            The payload data from mATRIC access point.
        """
        message = self._construct_message(payload)
        self._channel.send(message)
        self._channel.process()

    def close(self) -> None:
        """Closes the wiremq channel."""
        self._channel.close()


# Example usage
ap_manager = APManager(json_structure_file, wmq_channel_config_file)

# Get and print data for a 5G access point
ap_data_5g = ap_manager.getAPdata('5g')
ap_manager.pubAPdata(ap_data_5g)

# The Wi-Fi and Li-Fi data generation can be implemented similarly when their structures are defined.
