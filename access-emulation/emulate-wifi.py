import os
import json
from typing import Dict
import random
import string
import time
from pathlib import Path
import baseapemulator


class APEmulatorWiFi(baseapemulator.BaseAPEmulator):
    """
    Access Point Emulator for WiFi
    ==============================

    Emulates data published by a WiFi access point.

    Data is published to WireMQ/mATRIC using HTTP POST requests.

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

    def _populate_data(self) -> Dict:
        """Populates the AP JSON structure with random data.

        Returns
        -------
        data: Dict
            Assembled WiFi data payload.
        """
        data = json.loads(json.dumps(self._structure))

        # Populate WiFi structure with random data
        data["SSID"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["MACaddr"] = ':'.join(
            ['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

        # Populate bandwidth and utilization within specified ranges
        max_bandwidth_change = 1.0  # Define maximum change per iteration (e.g., 1 Gbps)
        if self._previous_bandwidth is None:
            data["results"]["Bandwidth"] = random.uniform(0, 9.5)
        else:
            new_bandwidth = self._previous_bandwidth + random.uniform(
                -max_bandwidth_change, max_bandwidth_change)
            data["results"]["Bandwidth"] = min(max(new_bandwidth, 0),
                                               9.5)  # Ensure within 0 to 9.5 Gbps range

        # Generate more realistic Utilization
        max_utilization_change = 5.0  # Define maximum change per iteration (e.g., 5%)
        if self._previous_utilization is None:
            data["results"]["Utilization"] = random.uniform(0.0, 100.0)
        else:
            new_utilization = self._previous_utilization + random.uniform(
                -max_utilization_change, max_utilization_change)
            data["results"]["Utilization"] = min(max(new_utilization, 0.0),
                                                 100.0)  # Ensure within 0% to 100% range

        # Update previous values
        self.previous_wifi_bandwidth = data["results"]["Bandwidth"]
        self.previous_wifi_utilization = data["results"]["Utilization"]

        data["results"]["HighSignal"] = random.uniform(0,
                                                       9.5)  # Highest recorded signal strength in Gbps
        data["results"]["RSSI"] = random.randint(-100,
                                                 0)  # Received Signal Strength Indicator
        data["results"]["HighRSSI"] = random.randint(-100,
                                                     0)  # Highest recorded RSSI
        data["results"]["Channel"] = random.randint(1, 11)  # WiFi channel
        data["results"]["Authentication"] = random.choice(
            ["WPA", "WPA2", "WEP", "None"])
        data["results"]["Encryption"] = random.choice(
            ["AES", "TKIP", "WEP", "None"])
        data["results"]["Manufacturer"] = ''.join(
            random.choices(string.ascii_letters, k=10))

        return data

# Define the path to the JSON structure file and channel configuration file.
path = Path(__file__).parent
json_structure_file = os.path.join(path, "wifi.json")

# URL to publish emulated monitoring data to
url = "http://127.0.0.1:8082/testapi/v1/monitoring/data"

# Create an instance of APManager
ap_manager = APEmulatorWiFi(
    json_structure_file,
    url
)

# Main event loop for emulator application
while True:
    #
    ap_manager.publish_data()
    time.sleep(5)
