#!/bin/sh

set -e
influx bucket create -n 5G -o UoB
influx bucket create -n Wifi -o UoB
influx bucket create -n Lifi -o UoB