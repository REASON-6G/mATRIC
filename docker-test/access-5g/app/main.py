# this code will generate 5G Nokia CLI data in json format
# the pubAPdata function should publish to wiremq the json object
# we need to implement the same generation for wifi and lifi
import os
import json
from typing import Dict
import random
import string
from datetime import datetime
import time
import logging
from pathlib import Path
from wiremq.gateway.endpoints import endpointfactory

# Define the path to the JSON structure file and channel configuration file.
path = Path(__file__).parent
json_structure_5g_file = os.path.join(path, "Nokia.json")
json_structure_wifi_file = os.path.join(path, "wifi.json")
wmq_channel_config_file = os.path.join(path, "wmq-channel.json")

def generate_random_time() -> Dict:
    """Generates a random time string with the format YYYY-MM-DDTHH:MM:SSZ

    Returns
    -------
    datetime: str
        Randomised datetime as a string.
    """
    year = random.randint(2020, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # to avoid issues with February
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:" \
           f"{second:02d}Z"

# Function to generate a unique identifier for matricID
def generate_matric_id() -> Dict:
    """Generates a random matricID string.

    Returns
    -------
    id: str
        Randomised identifier.
    """
    return ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=10))

# APManager class definition
class APManager:
    def __init__(self, structure_5g_file_path, structure_wifi_file_path, channel_config_file):
        self.structure_5g_file_path = structure_5g_file_path
        self.structure_wifi_file_path = structure_wifi_file_path
        self.channel_config_file = channel_config_file
        self.json_5g_structure = None
        self.json_wifi_structure = None
        self._initialise_channel(self.channel_config_file)
        self.triggered_behavior = False  # Flag to track if triggered behavior is active
        self.start_time = None  # Variable to store the start time of triggered behavior
        self.previous_5g_bandwidth = None
        self.previous_5g_utilization = None

    def _load_structure(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"The structure file {file_path} does not exist.")

    def control_behavior(self, start_behavior=True):
        """Control the behavior of increasing and decreasing bandwidth and utilization."""
        if start_behavior:
            # Start the triggered behavior
            self.triggered_behavior = True
            self.start_time = time.time()
        else:
            # Stop the triggered behavior
            self.triggered_behavior = False
            self.start_time = None

    def getAPdata(self, ap_type):
        if ap_type.lower() == '5g':
            if not self.json_5g_structure:
                self.json_5g_structure = self._load_structure(self.structure_5g_file_path)
            data = self.populate_5g_data()
        elif ap_type.lower() == 'wifi':
            if not self.json_wifi_structure:
                self.json_wifi_structure = self._load_structure(self.structure_wifi_file_path)
            data = self.populate_wifi_data()
        else:
            raise ValueError("AP type must be '5g' or 'wifi'.")

        if self.triggered_behavior:
            # Introduce time-based control for bandwidth and utilization
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            phase_duration = 10

            if elapsed_time < phase_duration:
                # WiFi bandwidth and utilization increasing phase
                data['results']['RadioStatistics']['Bandwidth'] += random.uniform(1, 5)
                data['results']['ChannelUtilization'] += random.uniform(1, 5)
            elif elapsed_time < 2 * phase_duration:
                # 5G and LiFi bandwidth and utilization increasing phase
                data['results']['RadioStatistics']['Bandwidth'] += random.uniform(1, 5)
                data['results']['ChannelUtilization'] += random.uniform(1, 5)
            elif elapsed_time < 3 * phase_duration:
                # WiFi bandwidth and utilization decreasing phase
                data['results']['RadioStatistics']['Bandwidth'] -= random.uniform(1, 5)
                data['results']['ChannelUtilization'] -= random.uniform(1, 5)


        data['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data['matricID'] = generate_matric_id()
        
        return data

    def _initialise_structure(self, structure_path: Dict) -> None:
        """Initialises structure for JSON payloads, reading the file from the
        provided path.

        Parameters
        ----------
        structure_path: str
            Directory path to the payload structure JSON file.

        """
        if os.path.exists(structure_path):
            with open(structure_path, 'r') as file:
                self.json_5g_structure = json.load(file)
        else:
            raise FileNotFoundError(f"The structure file {structure_path} "
                                    f"does not exist.")

    def _initialise_channel(self, channel_file_path: Dict) -> None:
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

        self._channel = endpointfactory.EndpointFactory().build(channel_config)

    def populate_5g_data(self) -> Dict:
        """Populates the 5G JSON structure with random data.

        Returns
        -------
        data: Dict
            Assembled 5G data payload.
        """
        data = json.loads(json.dumps(self.json_5g_structure))

        # Populate the JSON structure with random data
        data["distName"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["cellId"] = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        data["cellType"] = random.randint(1, 4)
        data["results"]["actualStartTime"] = generate_random_time()
        data["results"]["actualStopTime"] = generate_random_time()
        data["results"]["fwdTestDisp"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["result"] += ''.join(random.choices(string.ascii_letters, k=3))

        # Populate bandwidth and utilization
        max_bandwidth_change = 1.0  # (e.g., 1 Gbps)
        max_utilization_change = 5.0  # (e.g., 5%)

        if self.previous_5g_bandwidth is None:
            data["results"]["Bandwidth"] = random.uniform(0, 20)
        else:
            new_bandwidth = self.previous_5g_bandwidth + random.uniform(-max_bandwidth_change, max_bandwidth_change)
            data["results"]["Bandwidth"] = min(max(new_bandwidth, 0), 20)  # Ensure within 0 to 9.5 Gbps range

        if self.previous_5g_utilization is None:
            data["results"]["Utilization"] = random.uniform(0.0, 100.0)
        else:
            new_utilization = self.previous_5g_utilization + random.uniform(-max_utilization_change, max_utilization_change)
            data["results"]["Utilization"] = min(max(new_utilization, 0.0), 100.0)  # Ensure within 0% to 100% range

        self.previous_5g_bandwidth = data["results"]["Bandwidth"]
        self.previous_5g_utilization = data["results"]["Utilization"]


    # Populate the rfAntResults with random data
        rf_ant_results = data["results"]["rfAntResults"]
        rf_ant_results["antId"] = random.randint(1, 10)
        rf_ant_results["fwdETPw"] = random.uniform(0, 100)
        rf_ant_results["fwdETPdBm"] = random.uniform(-100, 0)
        rf_ant_results["fwdTPEerror"] = random.uniform(0, 10)  # Assuming LTE
        rf_ant_results["fwdTTPw"] = random.uniform(0, 100)     # Assuming LTE
        rf_ant_results["fwdTTPdBm"] = random.uniform(-100, 0)  # Assuming LTE
        rf_ant_results["rModId"] = random.randint(1, 100)
        rf_ant_results["rtwp"] = random.uniform(-100, 0)
        rf_ant_results["vswr"] = random.uniform(1, 3)
        rf_ant_results["rsi"] = random.uniform(-100, 0)        # Assuming NR
        rf_ant_results["sinr"] = random.uniform(0, 30)         # Assuming NR

        # Populate the rest of the fields with random data
        data["results"]["rvrsTestDisp"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["testOutcome"] += ''.join(random.choices(string.ascii_letters, k=3))
        data["results"]["testOutcomeAdditionalInfo"] += ''.join(random.choices(string.ascii_letters, k=10))
        data["results"]["sinr"] = random.uniform(0, 30)        # Assuming LTE

        return data

    def populate_wifi_data(self) -> Dict:
        data = json.loads(json.dumps(self.json_wifi_structure))
        
        # Populate WiFi structure with random data
        data["SSID"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["MACaddr"] = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
        data["results"]["Signal"] = random.randint(-100, 0)  # Signal strength in dBm
        data["results"]["HighSignal"] = random.randint(-100, 0)  # Highest recorded signal strength in dBm
        data["results"]["RSSI"] = random.randint(-100, 0)  # Received Signal Strength Indicator
        data["results"]["HighRSSI"] = random.randint(-100, 0)  # Highest recorded RSSI
        data["results"]["Channel"] = random.randint(1, 11)  # WiFi channel
        data["results"]["Location"]["LAT"] = random.uniform(-90, 90)  # Latitude
        data["results"]["Location"]["LON"] = random.uniform(-180, 180)  # Longitude
        data["results"]["Authentication"] = random.choice(["WPA", "WPA2", "WEP", "None"])
        data["results"]["Encryption"] = random.choice(["AES", "TKIP", "WEP", "None"])
        data["results"]["Manufacturer"] = ''.join(random.choices(string.ascii_letters, k=10))

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

    def close(self) -> None:
        """Closes the wiremq channel."""
        self._channel.close()


ap_manager = APManager(
    json_structure_5g_file,
    json_structure_wifi_file,
    wmq_channel_config_file
)


# while True:
#     # Get and print data for a 5G access point
#      command = input("Enter a command (start/stop/exit): ")
#     if command.lower() == "start":
#         ap_manager.control_behavior(start_behavior=True)
#         print("Triggered behavior started.")
#     elif command.lower() == "stop":
#         ap_manager.control_behavior(start_behavior=False)
#         print("Triggered behavior stopped.")
#     elif command.lower() == "exit":
#         break
#     else:
#         print("Invalid command. Use 'start' to start, 'stop' to stop, or 'exit' to exit.")

while True:
    ap_data_5g = ap_manager.getAPdata('5g')
    ap_manager.pubAPdata(ap_data_5g)
    time.sleep(5)

# Get and print data for a WiFi access point
# ap_data_wifi = ap_manager.getAPdata('wifi')
# ap_manager.pubAPdata(ap_data_wifi)
# ap_manager.close()
# The Wi-Fi and Li-Fi data generation can be implemented similarly when
# their structures are defined.
