import os
import json
from typing import Dict
import random
import string
import time
from pathlib import Path
import baseapemulator


class APEmulatorLiFi(baseapemulator.BaseAPEmulator):
    """
    Access Point Emulator for LiFi
    ==============================

    Emulates data published by a LiFi access point.

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
            Assembled LiFi data payload.
        """
        data = json.loads(json.dumps(self._structure))

        # Populate LiFi structure with random data
        data["SSID"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["MACaddr"] = ':'.join(
            ['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

        # Populate bandwidth and utilization within specified ranges
        max_bandwidth_change_lifi = 0.5  # Define maximum change per iteration for LiFi (e.g., 0.5 Gbps)
        if self._previous_bandwidth is None:
            data["results"]["Bandwidth"] = random.uniform(1, 3.5)
        else:
            new_bandwidth = self._previous_bandwidth + random.uniform(
                -max_bandwidth_change_lifi, max_bandwidth_change_lifi)
            data["results"]["Bandwidth"] = min(max(new_bandwidth, 1.0),
                                               3.5)  # Ensure within 1 to 3.5 Gbps range

        # Generate more realistic Utilization for LiFi
        max_utilization_change_lifi = 10.0  # Define maximum change per iteration for LiFi (e.g., 10%)
        if self._previous_utilization is None:
            data["results"]["Utilization"] = random.uniform(0, 100)
        else:
            new_utilization = self._previous_utilization + random.uniform(
                -max_utilization_change_lifi, max_utilization_change_lifi)
            data["results"]["Utilization"] = min(max(new_utilization, 0.0),
                                                 100.0)  # Ensure within 0% to 100% range

        # Update previous values for LiFi
        self.previous_lifi_bandwidth = data["results"]["Bandwidth"]
        self.previous_lifi_utilization = data["results"]["Utilization"]

        data["results"]["PacketStatistics"]["Transmitted"] = random.randint(0,
                                                                            10000)
        data["results"]["PacketStatistics"]["Received"] = random.randint(0,
                                                                         10000)
        data["results"]["PacketStatistics"]["Errors"] = random.randint(0, 100)
        data["results"]["ClientCount"] = random.randint(0, 500)
        data["results"]["ChannelUtilization"] = random.uniform(0, 100)
        data["results"]["TransmitPower"] = random.uniform(0, 100)
        data["results"]["Throughput"] = random.uniform(0, 10000)
        data["results"]["Latency"] = random.uniform(0, 100)
        data["results"]["Jitter"] = random.uniform(0, 50)
        data["results"]["PacketLoss"] = random.uniform(0, 100)
        data["results"]["AuthenticationRate"] = random.uniform(0, 100)
        data["results"]["DisassociationDeauthentication"] = random.randint(0,
                                                                           100)
        data["results"]["WIDSAlerts"] = random.randint(0, 50)
        data["results"]["ResourceUtilization"]["CPUUsage"] = random.uniform(0,
                                                                            100)
        data["results"]["ResourceUtilization"]["MemoryUsage"] = random.uniform(
            0, 100)
        data["results"]["RadioStatistics"]["Frequency"] = random.uniform(2400,
                                                                         2500)  # Example frequency range
        data["results"]["RadioStatistics"]["Modulation"] = random.choice(
            ["QAM", "PSK", "FSK"])
        data["results"]["RadioStatistics"]["Bandwidth"] = random.uniform(20,
                                                                         160)  # Example bandwidth values in MHz

        return data

# Define the path to the JSON structure file and channel configuration file.
path = Path(__file__).parent
json_structure_file = os.path.join(path, "lifi.json")

# URL to publish emulated monitoring data to
url = "http://access-lifi:8083/testapi/v1/monitoring/data"

# Create an instance of APManager
ap_manager = APEmulatorLiFi(
    json_structure_file,
    url
)

# Main event loop for emulator application
while True:
    #
    ap_manager.publish_data()
    time.sleep(5)
