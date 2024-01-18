import os
import json
from typing import Dict
import random
import string
from datetime import datetime
import time
import uuid
import requests


class BaseAPEmulator:
    """
    Base Access Point Emulator
    ==========================

    Base class for access point emulation. Holds standard methods for 5G, WiFi,
    LiFi etc. emulators to inherit.

    Each child class implements its own populate_data method.

    Parameters
    ----------
    _structure: Dict
        Structure of the AP data output.
    _url: str
        The URL to send emulated monitoring data to via POST requests.
    _previous_bandwidth: float
        Bandwidth from previous iteration.
    _previous_utilization: float
        Utilization from previous iteration.
    _trigger: bool
        Flag to trigger change in behaviour of the published emulation data.
    _start_time: float
        Time snapshot when trigger is initialized.

    """
    def __init__(self, structure_file_path: str, url: str):
        """AP Emulator intialization

        Parameters
        ----------
        structure_file_path: str
            Directory path to the JSON structure file.
        url: str
            The URL to send emulated monitoring data to via POST requests.
        """
        self._structure = self._load_structure(structure_file_path)
        self._url = url
        self._previous_bandwidth = 0
        self._previous_utilization = 0
        self._trigger = False
        self._start_time = 0

    def _load_structure(self, structure_file_path: str) -> Dict:
        """Loads the AP data structure from a JSON file.

        Parameters
        ----------
        structure_file_path: str
            Directory path to the JSON structure file.

        Returns
        -------
        structure: Dict
            Access point data structure.

        """
        if os.path.exists(structure_file_path):
            with open(structure_file_path, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(
                f"The structure file {structure_file_path} does not exist.")

    def _populate_data(self) -> Dict:
        """Populates the AP JSON structure with random data.

        To be implemented by child classes
        """
        pass

    def _generate_matric_id(self) -> str:
        """Generates a random matricID string.

        Returns
        -------
        id: str
            Randomised identifier.
        """
        return ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))

    def _generate_random_time(self) -> str:
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

    def _generate_access_point_data(self):
        """Generates emulated access point data.

        If trigger is set then bandwidth and utili\ation are increased

        Returns
        -------

        """
        data = self._populate_data()

        data['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data['matricID'] = self._generate_matric_id()

        if self._trigger:
            # Check if triggered behavior is active
            elapsed_time = time.time() - self._start_time
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
            "message_id": str(uuid.uuid4()),
            "type": "event",
            "payload": {
                "data": payload
            }
        }
        return message

    def publish_data(self) -> None:
        """Publishes the access point data.

        Constructs a wiremq message and uses the wiremq channel to send data to
        another channel.

        Parameters
        ----------
        payload: Dict
            The payload data from mATRIC access point.
        """
        payload = self._generate_access_point_data()
        message = self._construct_message(payload)
        print(requests.post(
            self._url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "5G-emulator"
            },
            data=message,
            timeout=5
        ))

    def toggle_trigger(self, enable_trigger=True) -> None:
        """Controls the behavior of increasing and decreasing bandwidth and
        utilization.

        Also starts timing the modified behaviour.

        Parameters
        ----------
        enable_trigger: bool
            Flag to trigger the modified publishing behaviour

        """
        if enable_trigger:
            # Start the triggered behavior
            self._trigger = True
            self._start_time = time.time()
        else:
            # Stop the triggered behavior
            self._trigger = False
            self._start_time = None
