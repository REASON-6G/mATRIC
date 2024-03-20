# Integration of WiFi AP to mATRIC (by C. Vrontos @SmartInternetLab, c.vrontos@bristol.ac.uk)
# This script does the following:
#   1. Dumps WiFi related data from the local machine.
#   2. Sends dumped string to mATRIC (URL:PORT) every X seconds.

import subprocess
import os
import json
from typing import Dict
import random
import string
import time
from datetime import datetime
from pathlib import Path
from urllib import request
import logging

logging.basicConfig(level=logging.INFO)

def publish_data(payload, destination) -> None:
    """Publishes the access point data.
    Constructs a wiremq message and uses the wiremq channel to send data to
    another channel.
    Parameters
    ----------
    payload: Dict
        The payload data from mATRIC access point.
    """
    #payload = self._generate_access_point_data()
    logging.info("publishing monitoring data")
    try:
        #data = parse.urlencode(json.dumps(payload)).encode()
        req = request.Request(
            #self._url,
            destination,
            headers={
                "Accept": "text/plain",
                "Content-Type": "text/plain",
                "User-Agent": "WiFi-AP"
            },
            data=json.dumps(payload).encode("utf-8")
        )
        response = request.urlopen(req)
        logging.debug(response.status)
    except BaseException:
        pass

# Set environment variables.
access_wifi = "10.128.2.174"
url = "http://"+access_wifi+":8082/testapi/v1/monitoring/data"

# Dump WiFi data: iw dev wlp3s0 station dump
wifi_dump = subprocess.run(['iw', 'dev', 'wlp3s0', 'station', 'dump'], stdout=subprocess.PIPE)

# Print human-readable format.
#print(wifi_dump.stdout.decode('utf-8'))

# Print raw string.
# print(wifi_dump)

# Send data to mATRIC.
publish_data(wifi_dump, url)