import os
import json
from typing import Dict
import random
import string
import time
from pathlib import Path
import math
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

    STATIONS = [
        "f4:7b:09:f0:9d:f3",
        "c8:3a:35:a4:06:9d",
        "a9:a1:bb:9f:e2:12"
    ]

    def _random(self,
                min: float,
                max: float,
                x_scale: float = 1,
                noise: float = 0.05) -> float:
        """
        Generates a psuedo-random number

        Numbers are based on variations of a sine wave which is calculated
        from the last 2 seconds of the current time.

        The noise component of the wave is randomised
        """
        seed = time.time() % 100
        rads = 200*3.1415926535/seed
        jitter = random.uniform(-noise, noise)
        # Produce a sine wave between 0 and 1 and add jitter
        wave = 0.5*math.sin(rads/x_scale) + 1 + jitter

        # Scale the sine wave from the user parameters
        result = min + (max - min)*wave 
        if result < 0:
            result = 0
        print(seed)
        return result

    def _generate_station_data(self, station_index: int) -> str:
        """Generates randomised monitoring data from the access point.

        Parameters
        ----------
        station_index: int
            Identifier for the station in STATIONS to use

        Returns
        -------
        data: str
            monitoring data
        """
        current_time = time.time()
        data = f"Station {self.STATIONS[station_index]} (on wlp3s0)\n"
        data += f"       inactive time: {self._random(1, 50000)}\n"
        data += f"       rx bytes:      {self._random(1, 250000)}\n"
        data += f"       rx packets:    {self._random(1, 40000000)}\n"
        data += f"       tx bytes:    {self._random(0.1, 50000000)}\n"
        data += f"       tx_packets:    {self._random(0.1, 50000)}\n"
        data += f"       tx retries:    {self._random(0.01, 100)}\n"
        data += f"       tx failed:    {int(self._random(0.01, 5))}\n"
        data += f"       rx drop misc:    {int(self._random(1, 2))}\n"
        data += f"       signal:    -{int(self._random(25, 100))} [-{int(self._random(20, 120))}, -{int(self._random(20, 120))}] dBm\n"
        data += f"       signal avg:    {self._random(1, 150)}\n"
        data += f"       tx bitrate:    {self._random(0.5, 10)}\n"
        data += f"       tx duration:    {self._random(0.5, 10)} us\n"
        data += f"       rx bitrate:    {self._random(1, 200)}\n"
        data += f"       rx duration:    {self._random(1, 200000)} us\n"
        data += f"       last ack signal:    {self._random(1, 100)}\n"
        data += f"       avg ack signal:    {self._random(1, 80)}\n"
        data += f"       authorized:    yes\n"
        data += f"       authenticated:    yes\n"
        data += f"       associated:    yes\n"
        data += f"       preamble:    long\n"
        data += f"       WMM/WME:    yes\n"
        data += f"       MFP:    no\n"
        data += f"       TDLS peer:    no\n"
        data += f"       DTIM period:    2\n"
        data += f"       beacon interval:    100\n"
        data += f"       short slot time:    yes\n"
        data += f"       connected time:    {self._random(0.01, 1500)}\n"
        data += f"       associated at [boottime]:    {current_time - 13696145}\n"
        data += f"       associated at:    {current_time - 13696145}\n"
        data += f"       current time:    {current_time} ms\n"

        return data


    def _populate_data(self) -> Dict:
        """

        """
        data = ""
        for station_index in range(0, 2):
            data += self._generate_station_data(station_index)
        
        return data

        

# Define the path to the JSON structure file and channel configuration file.
path = Path(__file__).parent
json_structure_file = os.path.join(path, "wifi.json")

# URL to publish emulated monitoring data to
url = "http://access-wifi:8082/testapi/v1/monitoring/data"

# Create an instance of APManager
ap_manager = APEmulatorWiFi(
    json_structure_file,
    url
)

# Main event loop for emulator application
while True:
    #
    ap_manager.publish_data()
    # print(ap_manager._generate_station_data(0))
    time.sleep(5)
