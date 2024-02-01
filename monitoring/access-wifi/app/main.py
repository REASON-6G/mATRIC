import os
import json
from typing import (
    Dict,
    List
)
import random
import string
from datetime import datetime
import time
import logging
from pathlib import Path
from wiremq.gateway.endpoints import endpointfactory
from wiremq.gateway.messages import messagefactory

logger = logging.getLogger("channel_wifi_logger")

# Define the path to the JSON structure file and channel configuration file.
path = Path(__file__).parent
config_file = os.path.join(path, "config.json")


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
    def __init__(self, config_file):
        self._config_file = config_file
        self._channel_config = None
        self._serviceactivator_config = None
        self._monitoring_config = None
        self._channel = None
        self._serviceactivator = None
        self._initialise_configs(config_file)
        self._initialise_channel()
        self._initialise_serviceactivator()
        self._mf = messagefactory.MessageFactory()

    def _initialise_configs(self, config_file_path: str) -> None:
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
        self._monitoring_config = config["monitoring_config"]

    def _initialise_channel(self) -> None:
        """Initialises a wiremq channel.

        This channel is used for outbound communication to another channel, on
        a P2P basis.
        """

        self._channel = endpointfactory.EndpointFactory().build(
            self._channel_config)
        logger.test(f"WireMQ Channel listening on port "
                    f"{self._channel_config['port']}")

    def _initialise_serviceactivator(self):
        """Initialises the Service Activator.

        This is used as the HTTP endpoint for the application. Incoming
        messages are forwarded to the Channel.
        """
        self._serviceactivator = endpointfactory.EndpointFactory().build(
            self._serviceactivator_config)
        self._serviceactivator.start_server()
        logger.test(f"WireMQ listening for HTTP messages on port "
                    f"{self._serviceactivator_config['http_port']}")

    def _prepare_payload_data(self, monitoring_data: Dict) -> Dict:
        """Prepares the payload ready to send to the aggregator.

        Parameters
        ----------
        monitoring_data: Dict
            Monitoring data from the access point.

        Returns
        -------
        payload_data: Dict
            Payload to be attached to the outgoing message to the aggregator.
        """
        payload_data = monitoring_data
        payload_data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        payload_data["matricID"] = generate_matric_id()
        payload_data["Aptech"] = "wifi"

        return payload_data

    def _construct_message(self, payload_data: Dict) -> Dict:
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
        header = {
            "sender_ip": "127.0.0.1",
            "sender_port": 10002,
            "dest_ip": "127.0.0.1",
            "dest_port": 10000,
            "protocol_version": "0.0.1"
        }
        payload = {
            "data": payload_data
        }
        message = self._mf.eventmessage(header, payload)
        return message

    def _parse_monitoring_data(self, data: str) -> List:
        """Parses raw text from monitoring stream, converting it to JSON.

        Parameters
        ----------
        data: str
            Raw data string from the WiFi monitoring

        Returns
        -------
        data_json: Dict
            Computed dictionary containing monitoring data.
        """
        data_json = []
        current_station = None
        config = self._monitoring_config

        for line in data.split('\n'):
            if config['station_identifier'] in line:
                if current_station:
                    data_json.append(current_station)
                current_station = {'mac_address': line.split()[1],
                                   'details': {}}
            elif current_station and config['delimiter'] in line:
                key, value = map(str.strip, line.split(config['delimiter'], 1))
                if key == config['mac_address_key']:
                    current_station['mac_address'] = value
                else:
                    current_station['details'][key] = value

        if current_station:
            data_json.append(current_station)

        logging.critical(json.dumps(data_json, indent=2))

        return data_json

    def _handle_http_message(self, msg: Dict):
        """Controls the HTTP interface

        Reads the message payload for route information and responds
        accordingly.

        Currently, this application has implemented:

          - monitoring/data: POST interface, for APs to submit monitoring data
                             to. Data is processed and forwarded to the
                             aggregator application.

        Parameters
        ----------
        msg: Dict
            Incoming command message with HTTP fields

        """
        service = msg["payload"]["service"]
        command = msg["payload"]["command"]

        if service == "monitoring" and command == "data":
            # Monitoring data submitted via HTTP

            # Respond to the access point with a 201 success
            self._respond_monitoring_http(msg)

            # Extract the monitoring data
            try:
                monitoring_data = \
                    self._parse_monitoring_data(msg["payload"]["data"])
            except json.decoder.JSONDecodeError as e:
                logger.error(f"unable to decode message: {e}")
                return
            except BaseException as e:
                logger.error(f"unable to decode message: {e} {type(e)}")
                return

            # Supplement with mATRIC data
            for station in monitoring_data:
                payload_data = self._prepare_payload_data(station)

                # Prepare the message
                message = self._construct_message(payload_data)

                # Forward the monitoring data to the aggregator
                self._channel.send(message)

    def _respond_monitoring_http(self, msg: Dict):
        """Responds to the access point with a HTTP Response.

        The service activator stores the address of the remote client, which
        is identified by the tx_correlation_id.

        Parameters
        ----------
        msg: Dict
            The HTTP message to respond to.
        """
        header = {
            "correlation_id": msg["message_id"],
            "tx_correlation_id": msg["tx_id"],
            "error_code": 201,
            "error_message": "OK",
            "protocol_version": "0.0.1",
            "sender_ip": "127.0.0.1",
            "sender_port": 8082,
            "dest_ip": msg["sender_ip"],
            "dest_port": msg["sender_port"]
        }
        payload = {"data": "OK"}
        response = self._mf.serviceresponsemessage(header, payload)
        self._serviceactivator.send(response)

    def publish_access_point_data(self, payload: Dict) -> None:
        """Publishes the access point data.

        Constructs a wiremq message and uses the WireMQ channel to send data to
        another channel.

        Parameters
        ----------
        payload: Dict
            The payload data from the access point.
        """
        message = self._construct_message(payload)
        self._channel.send(message)

    def receive(self):
        """Generic method to receive messages on WireMQ endpoints and handle
        them.
        """

        # Run the service activator, any incoming HTTP messages will be
        # automatically forwarded to the channel
        self._serviceactivator.process()

        # Receive messages on the channel
        msgs = self._channel.receive()
        for msg in msgs:
            logger.test(f"WireMQ Channel received {msg.get('message_id')} from"
                        f" {msg.get('sender_alias')}")
            if msg.get("tx_id") and msg.get("method") == "POST":
                self._handle_http_message(msg)

    def close(self) -> None:
        """Closes the wiremq channel."""
        self._channel.close()
        self._serviceactivator.close()


if __name__ == "__main__":

    # Create an instance of APManager
    ap_manager = APManager(config_file)

    while True:
        ap_manager.receive()
        time.sleep(0.05)

    # Cleanup and close the wiremq channel
    ap_manager.close()
