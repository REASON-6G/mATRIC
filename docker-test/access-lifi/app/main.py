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
from wiremq.gateway.messages import messagefactory

logger = logging.getLogger("channel_lifi_logger")

# Define the path to the JSON structure file and channel configuration file.
path = Path(__file__).parent
json_structure_5g_file = os.path.join(path, "Nokia.json")
json_structure_wifi_file = os.path.join(path, "wifi.json")
json_structure_lifi_file = os.path.join(path, "lifi.json")
wmq_config_file = os.path.join(path, "wmq.json")


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
    def __init__(self, structure_path, wmq_config_file):
        self.structure_path = structure_path
        self.wmq_config_file = wmq_config_file
        self.json_structure = None
        self._channel_config = None
        self._serviceactivator_config = None
        self._channel = None
        self._serviceactivator = None
        self._initialise_wmq_config(wmq_config_file)
        self._initialise_channel()
        self._initialise_serviceactivator()
        self._mf = messagefactory.MessageFactory()

    def _load_structure(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"The structure file {file_path} does not exist.")

    def receive(self):
        """Generic method to receive messages on WireMQ endpoints and handle
        them.

        Returns
        -------

        """

        # Run the service activator, any incoming HTTP messages will be
        # automatically forwarded to the channel
        self._serviceactivator.process()

        # Receive messages on the channel
        msgs = self._channel.receive()
        import json
        for msg in msgs:
            # HTTP messages
            if msg.get("tx_id") and msg.get("method") == "POST":
                self.handle_http_message(msg)

    def handle_http_message(self, msg: Dict):
        """

        Parameters
        ----------
        message

        Returns
        -------

        """
        print("AAAAAAAAAAAAAAA")
        print(json.dumps(msg, indent=2))
        self.respond_monitoring_http(msg)

    def respond_monitoring_http(self, msg: Dict):
        """

        Parameters
        ----------
        msg

        Returns
        -------

        """
        header = {
            "correlation_id": msg["message_id"],
            "tx_correlation_id": msg["tx_id"],
            "error_code": 201,
            "error_message": "OK",
            "protocol_version": "0.0.1",
            "sender_ip": "127.0.0.1",
            "sender_port": 8083,
            "dest_ip": msg["sender_ip"],
            "dest_port": msg["sender_port"]
        }
        payload = {"data": "OK"}
        response = self._mf.serviceresponsemessage(header, payload)
        self._serviceactivator.send(response)



    def getAPdata(self):
        if not self.json_structure:
            self.json_structure = self._load_structure(self.structure_path)
        data = self.populate_data()

        # Receive the most recent message on the channel
        print("getting AP data")
        self._serviceactivator.process()
        msgs = self._channel.receive()
        for msg in msgs:
            print("AAAAAAAAAAAAAAA")
            print(msg)
        if msgs:
            msg = msgs[-1]
            logger.test(f"Received message: {msg}")
            return msg

        data['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data['matricID'] = generate_matric_id()

        return None

    def _initialise_structure(self, structure_path: str) -> None:
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

    def _initialise_wmq_config(self, config_file_path: str) -> None:
        """Loads the config file for WireMQ components

        Parameters
        ----------
        config_file_path: str
            Directory path to the WMQ configuration JSON file.
        """
        with open(config_file_path, "rb") as f:
            config = json.load(f)

        self._channel_config = config["channel_config"]
        self._serviceactivator_config = config["serviceactivator_config"]

    def _initialise_channel(self) -> None:
        """Initialises a wiremq channel.

        This channel is used for outbound communication to another channel, on
        a P2P basis.
        """

        self._channel = endpointfactory.EndpointFactory().build(
            self._channel_config)

    def _initialise_serviceactivator(self):
        """Initialises the Service Activator.

        This is used as the HTTP endpoint for the application. Incoming
        messages are forwarded to the Channel.
        """
        self._serviceactivator = endpointfactory.EndpointFactory().build(
            self._serviceactivator_config)
        self._serviceactivator.start_server()

    def populate_data(self) -> Dict:
        data = json.loads(json.dumps(self.json_structure))
        
        # Populate LiFi structure with random data
        data["SSID"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["MACaddr"] = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
        data["results"]["SignalStrengthRSSI"] = random.randint(-100, 0)
        data["results"]["Bitrate"] = random.randint(1, 1000)
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
        # self._channel.send(message)

    def close(self) -> None:
        """Closes the wiremq channel."""
        self._channel.close()


# Create an instance of APManager
ap_manager = APManager(
    json_structure_lifi_file,
    wmq_config_file
)

# # Command-line interface to control the behavior
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
    logger.test("LiFI monitoring looping")
    ap_manager.receive()
    #ap_data = ap_manager.getAPdata()
    # if ap_data:
    #     ap_manager.pubAPdata(ap_data)
    time.sleep(0.5)


# Cleanup and close the wiremq channel
ap_manager.close()
