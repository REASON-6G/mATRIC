import os
import json
from typing import Dict
import random
import string
import time
from pathlib import Path
import baseapemulator


class APEmulator5G(baseapemulator.BaseAPEmulator):
    """
    Access Point Emulator for 5G
    ============================

    Emulates data published by a 5G access point.

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
            Assembled 5G data payload.
        """
        data = json.loads(json.dumps(self._structure))

        # Populate the JSON structure with random data
        data["distName"] += ''.join(random.choices(string.ascii_letters, k=5))
        data["cellId"] = ''.join(
            random.choices(string.ascii_letters + string.digits, k=8))
        data["cellType"] = random.randint(1, 4)
        data["results"]["actualStartTime"] = self._generate_random_time()
        data["results"]["actualStopTime"] = self._generate_random_time()
        data["results"]["fwdTestDisp"] += ''.join(
            random.choices(string.ascii_letters, k=3))
        data["results"]["result"] += ''.join(
            random.choices(string.ascii_letters, k=3))

        # Populate bandwidth and utilization
        max_bandwidth_change_5g = 2.0  # Define maximum change per iteration for 5G (e.g., 2 Gbps)
        if self._previous_bandwidth is None:
            data["results"]["Bandwidth"] = random.uniform(0.0, 20.0)
        else:
            new_bandwidth = self._previous_bandwidth + random.uniform(
                -max_bandwidth_change_5g, max_bandwidth_change_5g)
            data["results"]["Bandwidth"] = min(max(new_bandwidth, 0.0),
                                               20.0)  # Ensure within 0 to 20 Gbps range

        # Generate more realistic Utilization for 5G
        max_utilization_change_5g = 10.0  # Define maximum change per iteration for 5G (e.g., 10%)
        if self._previous_utilization is None:
            data["results"]["Utilization"] = random.uniform(0.0, 100.0)
        else:
            new_utilization = self._previous_utilization + random.uniform(
                -max_utilization_change_5g, max_utilization_change_5g)
            data["results"]["Utilization"] = min(max(new_utilization, 0.0),
                                                 100.0)  # Ensure within 0% to 100% range

        # Update previous values
        self.previous_bandwidth = data["results"]["Bandwidth"]
        self.previous_utilization = data["results"]["Utilization"]

        # Populate the rfAntResults with random data

        rf_ant_results = data["results"]["rfAntResults"]
        rf_ant_results["antId"] = random.randint(1, 10)
        rf_ant_results["fwdETPw"] = random.uniform(0, 100)
        rf_ant_results["fwdETPdBm"] = random.uniform(-100, 0)
        rf_ant_results["fwdTPEerror"] = random.uniform(0, 10)  # Assuming LTE
        rf_ant_results["fwdTTPw"] = random.uniform(0, 100)  # Assuming LTE
        rf_ant_results["fwdTTPdBm"] = random.uniform(-100, 0)  # Assuming LTE
        rf_ant_results["rModId"] = random.randint(1, 100)
        rf_ant_results["rtwp"] = random.uniform(-100, 0)
        rf_ant_results["vswr"] = random.uniform(1, 3)
        rf_ant_results["rsi"] = random.uniform(-100, 0)  # Assuming NR
        rf_ant_results["sinr"] = random.uniform(0, 30)  # Assuming NR

        # Populate the rest of the fields with random data
        data["results"]["rvrsTestDisp"] += ''.join(
            random.choices(string.ascii_letters, k=3))
        data["results"]["testOutcome"] += ''.join(
            random.choices(string.ascii_letters, k=3))
        data["results"]["testOutcomeAdditionalInfo"] += ''.join(
            random.choices(string.ascii_letters, k=10))
        data["results"]["sinr"] = random.uniform(0, 30)  # Assuming LTE

        return data

if __name__ == "__main__":
    # Define the path to the JSON structure file and channel configuration file.
    path = Path(__file__).parent
    json_structure_file = os.path.join(path, "nokia.json")

    # URL to publish emulated monitoring data to
    url = "http://access-5g:8081/testapi/v1/monitoring/data"

    # Create an instance of APManager
    ap_manager = APEmulator5G(
        json_structure_file,
        url
    )

    # Main event loop for emulator application
    while True:
        #
        ap_manager.publish_data()
        time.sleep(5)
