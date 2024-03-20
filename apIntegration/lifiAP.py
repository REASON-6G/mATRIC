# Integration of LiFi AP to mATRIC (by C. Vrontos @SmartInternetLab, c.vrontos@bristol.ac.uk)
# This script does the following:
#   1. Dumps WiFi related data from the local machine.
#   2. Sends dumped string to mATRIC (URL:PORT) every X seconds.
#   This script runs on the lifi AP

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
    logging.info("publishing monitoring data")
    logging.info(payload)
    try:
        #data = parse.urlencode(json.dumps(payload)).encode()
        req = request.Request(
            #self._url,
            destination,
            headers={
                "Accept": "text/plain",
                "Content-Type": "text/plain",
                "User-Agent": "LiFi-AP"
            },
            data=payload
        )
        response = request.urlopen(req)
        logging.info(response.status)
    except BaseException:
        pass

def get_data():
     # Dump LiFi data: iw dev wlp3s0 station dump
    lifi_data = subprocess.run(['iw', 'dev', 'wlan0', 'station', 'dump'], stdout=subprocess.PIPE)
    
    return lifi_data.stdout


# Set environment variables.
access_lifi = "10.128.2.174"
url = "http://"+access_lifi+":8083/testapi/v1/monitoring/data"

while True:
  try:
    payload = get_data()
    logging.info(payload)
    if not payload:
      payload = b"no data"
    publish_data(payload, url)
  except BaseException:
    pass
  time.sleep(5)