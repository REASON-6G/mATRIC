# mATRIC Documentation
mATRIC is multi-Access Technology Intelligent Controller

# Description 
This repository, containing mATRIC implementation platform, has been made open-source as part of the REASON project, which is Realising Enabling Architectures and Solutions for Open Networks.
mATRIC is an intelligent RAN controller supporting multiple access technologies.

**The mATRIC platform supports the following capabilities:**

- Real-time and near real-time scenarios.
- Cellular and non-cellular access technologies – _5G, WiFi, LiFi_.
- Monitoring and data analytics.
- Control and optimisation of RAN resources.
- On-demand deployment.


# Architecture

mATRIC is comprised of 5 building blocks

1. BB1
2. BB2
3. BB3
4. BB4
5. BB5
 
![alt text](/matric.png)

# Deployment of matric

docker compose build to build the key containers of Matric

Command to build mATRIC

docker compose -up build

- emulate5g
- emulatewifi
- emylatelifi
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
