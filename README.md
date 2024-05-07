![mATRIC update logo](https://github.com/hpn-bristol/mATRIC/assets/63154875/5692d351-818e-48c2-834d-5d735871329d)

    multi-Access Technology Intelligent Controller

# Basic overview 
This repository host the mATRIC software implementation platform, an intelligent RAN controller developed under the [![Static Badge](https://img.shields.io/badge/REASON-project)](https://reason-open-networks.ac.uk/about/) project to support multiple wireless access technologies.


**The mATRIC platform supports the following capabilities:**

- Real-time and near real-time scenarios.
- Cellular and non-cellular access technologies – _5G, WiFi, LiFi_.
- Monitoring, intelligence and data analytics.
- Control and optimisation of RAN resources.


# Architecture

mATRIC is comprised of 3 building blocks

1. mATRIC Broker
   (Description)

2. mATRIC OPEN API
   (Description)

3. mATRIC mAT Manager
   (Description)

 
![alt text](/matric.png)

# Deployment of matric

docker compose build to build the key containers of mATRIC

Command to build mATRIC

docker compose -up build

- emulate5g
- emulatewifi
- emulatelifi
- accessaggregator
- access5G
- accessWifi

If you want to run a specific configuration of mATRIC you need to modify the docker-compose.yml file accordigly.

# InfluxDB Configuration

# Access Point Integration

# Database Query Example

# mATRIC usage documentation

# API for Access Point Integration

This API endpoint provides mATRIC users to integrate their access points with the platform. The below guidance will assist with steps for integrating one or many access points with mATRIC.

# API for Data Access

# API for RAN Control

# How to contribute
