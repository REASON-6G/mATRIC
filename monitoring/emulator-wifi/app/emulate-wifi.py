from typing import Dict
import random
import time
import math
import logging
from urllib import request

logging.basicConfig(level=logging.INFO)


class APEmulatorWiFi:
    """
    Access Point Emulator for WiFi
    ==============================

    Emulates data published by a WiFi access point.

    Data is published to WireMQ/mATRIC using HTTP POST requests.

    Attributes
    ----------
    _url: str
        The URL to send emulated monitoring data to via POST requests.

    """

    STATIONS = [
        "f4:7b:09:f0:9d:f3",
        "c8:3a:35:a4:06:9d",
        "a9:a1:bb:9f:e2:12"
    ]

    def __init__(self, url: str):
        self._url = url

    def _random(self,
                min: float,
                max: float,
                x_scale: float = 1,
                noise: float = 0.05) -> float:
        """Generates a psuedo-random number following a time-based sine wave.

        Numbers are based on variations of a sine wave which is calculated
        from the last 2 seconds of the current time.

        The noise component of the wave is randomised

        Parameters
        ----------
        min: float
            Minimum value of the noiseless waveform (with noise the
            calculated value cannot go below 0)
        max: float
            Maximum number of the noiseless waveform
        x_scale: float
            The horizontal scale factor of the waveform
        noise: float
            The noise factor to apply to the waveform (should be between 0 and
            0.5, 0.1 is recommended as a sensible maximum)
        """
        seed = time.time() % 100
        rads = seed * 2 * 3.1415926535 / 100
        jitter = random.uniform(-noise, noise)
        # Produce a sine wave between 0 and 1 and add jitter
        wave = 0.5*(math.sin(rads/x_scale) + 1) + \
               0.25*(math.sin(rads/(5*x_scale)) + 1) + jitter

        # Scale the sine wave from the user parameters
        result = min + (max - min)*wave 
        if result < 0:
            result = 0
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

    def _populate_data(self) -> str:
        """

        """
        data = ""
        for station_index in range(0, 2):
            data += self._generate_station_data(station_index)
        
        return data

    def publish_data(self) -> None:
        """Publishes the access point data.

        Constructs a HTTP request and sends it to the monitoring app.

        Parameters
        ----------
        payload: Dict
            The payload data from mATRIC access point.
        """
        payload = self._populate_data()
        logging.info(f"publishing monitoring data to {self._url}")
        try:
            req = request.Request(
                self._url,
                headers={
                    "Accept": "text/plain",
                    "Content-Type": "text/plain",
                    "User-Agent": "AP-emulator"
                },
                data=payload.encode("utf-8")
            )
            response = request.urlopen(req, timeout=10)
            logging.info(response.status)
        except BaseException as e:
            logging.warning(e)
            pass


# URL to publish emulated monitoring data to
url = "http://access-wifi:8082/testapi/v1/monitoring/data"

# Create an instance of APManager
ap_manager = APEmulatorWiFi(url)
# Main event loop for emulator application
while True:
    ap_manager.publish_data()
    time.sleep(5)
