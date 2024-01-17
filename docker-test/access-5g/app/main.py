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
json_structure_lifi_file = os.path.join(path, "lifi.json")
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
    def __init__(self, structure_5g_file_path, structure_wifi_file_path, structure_lifi_file_path, channel_config_file):
        self.structure_5g_file_path = structure_5g_file_path
        self.structure_wifi_file_path = structure_wifi_file_path
        self.structure_lifi_file_path = structure_lifi_file_path
        self.json_lifi_structure = None
        self.channel_config_file = channel_config_file
        self.previous_5g_bandwidth = None
        self.previous_5g_utilization = None
        self.json_5g_structure = None
        self.json_wifi_structure = None
        self._channel = None  # Initialize the channel as None
        self.triggered_behavior = False
        self.start_time = None
        
        try:
            self._initialise_channel(self.channel_config_file)
        except Exception as e:
            logging.error(f"Failed to initialize the channel: {e}")

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
        elif ap_type.lower() == 'lifi':
            if not self.json_lifi_structure:
                self.json_lifi_structure = self._load_structure(self.structure_lifi_file_path)
            data = self.populate_lifi_data()
        else:
            raise ValueError("AP type must be '5g', 'wifi', or 'lifi'.")

        data['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data['matricID'] = generate_matric_id()

        if self.triggered_behavior:
            # Check if triggered behavior is active
            elapsed_time = time.time() - self.start_time
            if 0 <= elapsed_time < 10:
                # WiFi bandwidth and utilization go up for 10 seconds
                data['results']['Bandwidth'] += random.uniform(1, 5)
                data['results']['Utilization'] += random.uniform(1, 5)
            elif 10 <= elapsed_time < 20:
                # 5G and LiFi bandwidth and utilization go up for 10 seconds
                data['results']['Bandwidth'] += random.uniform(1, 5)
                data['results']['Utilization'] += random.uniform(1, 5)
            elif 20 <= elapsed_time < 30:
                # WiFi bandwidth and utilization go down for 10 seconds
                data['results']['Bandwidth'] -= random.uniform(1, 5)
                data['results']['Utilization'] -= random.uniform(1, 5)

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
        max_bandwidth_change_5g = 2.0  # Define maximum change per iteration for 5G (e.g., 2 Gbps)
        if self.previous_5g_bandwidth is None:
            data["results"]["Bandwidth"] = random.uniform(0.0, 20.0)
        else:
            new_bandwidth = self.previous_5g_bandwidth + random.uniform(-max_bandwidth_change_5g, max_bandwidth_change_5g)
            data["results"]["Bandwidth"] = min(max(new_bandwidth, 0.0), 20.0)  # Ensure within 0 to 20 Gbps range

        # Generate more realistic Utilization for 5G
        max_utilization_change_5g = 10.0  # Define maximum change per iteration for 5G (e.g., 10%)
        if self.previous_5g_utilization is None:
            data["results"]["Utilization"] = random.uniform(0.0, 100.0)
        else:
            new_utilization = self.previous_5g_utilization + random.uniform(-max_utilization_change_5g, max_utilization_change_5g)
            data["results"]["Utilization"] = min(max(new_utilization, 0.0), 100.0)  # Ensure within 0% to 100% range

        # Update previous values for 5G
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
        
        # Populate bandwidth and utilization within specified ranges
        data["results"]["Bandwidth"] = random.uniform(0, 9.5)  # 0 to 9.5 Gbps for WiFi
        data["results"]["Utilization"] = random.uniform(0, 100)  # 0% to 100%
        
        data["results"]["HighSignal"] = random.uniform(0, 9.5)  # Highest recorded signal strength in Gbps
        data["results"]["RSSI"] = random.randint(-100, 0)  # Received Signal Strength Indicator
        data["results"]["HighRSSI"] = random.randint(-100, 0)  # Highest recorded RSSI
        data["results"]["Channel"] = random.randint(1, 11)  # WiFi channel
        data["results"]["Authentication"] = random.choice(["WPA", "WPA2", "WEP", "None"])
        data["results"]["Encryption"] = random.choice(["AES", "TKIP", "WEP", "None"])
        data["results"]["Manufacturer"] = ''.join(random.choices(string.ascii_letters, k=10))

        return data

    def populate_lifi_data(self) -> Dict:
        data = json.loads(json.dumps(self.json_lifi_structure))
        
        # Populate LiFi structure with random data
        data["SSID"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["MACaddr"] = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
        
        # Populate bandwidth and utilization within specified ranges
        data["results"]["Bandwidth"] = random.uniform(1, 3.5)  # 1 to 3.5 Gbps for LiFi
        data["results"]["Utilization"] = random.uniform(0, 100)  # 0% to 100%
        
        data["results"]["PacketStatistics"]["Transmitted"] = random.randint(0, 10000)
        data["results"]["PacketStatistics"]["Received"] = random.randint(0, 10000)
        data["results"]["PacketStatistics"]["Errors"] = random.randint(0, 100)
        data["results"]["ClientCount"] = random.randint(0, 500)
        data["results"]["ChannelUtilization"] = random.uniform(0, 100)
        data["results"]["TransmitPower"] = random.uniform(0, 100)
        data["results"]["Throughput"] = random.uniform(0, 10000)
        data["results"]["Latency"] = random.uniform(0, 100)
        data["results"]["Jitter"] = random.uniform(0, 50)
        data["results"]["PacketLoss"] = random.uniform(0, 100)
        data["results"]["AuthenticationRate"] = random.uniform(0, 100)
        data["results"]["DisassociationDeauthentication"] = random.randint(0, 100)
        data["results"]["WIDSAlerts"] = random.randint(0, 50)
        data["results"]["ResourceUtilization"]["CPUUsage"] = random.uniform(0, 100)
        data["results"]["ResourceUtilization"]["MemoryUsage"] = random.uniform(0, 100)
        data["results"]["RadioStatistics"]["Frequency"] = random.uniform(2400, 2500)  # Example frequency range
        data["results"]["RadioStatistics"]["Modulation"] = random.choice(["QAM", "PSK", "FSK"])
        data["results"]["RadioStatistics"]["Bandwidth"] = random.uniform(20, 160)  # Example bandwidth values in MHz

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


# Create an instance of APManager
ap_manager = APManager(
    json_structure_5g_file,
    json_structure_wifi_file,
    json_structure_lifi_file,
    wmq_channel_config_file
)

# Command-line interface to control the behavior
# while True:
#     command = input("Enter a command (start/stop/exit): ")
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
    # Get and print data for a 5G access point
    ap_data_5g = ap_manager.getAPdata('5g')
    ap_manager.pubAPdata(ap_data_5g)
    time.sleep(5)



# Get and print data for a WiFi access point
# ap_data_wifi = ap_manager.getAPdata('wifi')
# ap_manager.pubAPdata(ap_data_wifi)
# ap_manager.close()
# The Wi-Fi and Li-Fi data generation can be implemented similarly when
# their structures are defined.
