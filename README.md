![mATRIC update logo](https://github.com/hpn-bristol/mATRIC/assets/63154875/5692d351-818e-48c2-834d-5d735871329d)

mATRIC is multi-Access Technology Intelligent Controller

# Basic overview 
This repository host the mATRIC software implementation platform, an intelligent RAN controller developed under the [![Static Badge](https://img.shields.io/badge/REASON-project)](https://reason-open-networks.ac.uk/about/) project to support multiple wireless access technologies.


**The mATRIC platform supports the following capabilities:**

- Real-time and near real-time scenarios.
- Cellular and non-cellular access technologies – _5G, WiFi, LiFi_.
- Monitoring, intelligence and data analytics.
- Control and optimisation of RAN resources.


# Architecture

**mATRIC platform consist of 3 key building blocks.** <br>
The platform is compatible with standard ORAN and 3GPP interfaces. The E2 and O1 interfaces provide access to the mATRIC platform, enabling it to gather metrics and interact with RAN nodes. This functionality enables the integration of multiple access technologies within the platform. <br>
The building blocks are as follows: <br>

1. **mATRIC Broker** <br>
The broker manages data integration in mATRIC. The broker components include AT Registry database, mATRIC database, and WireMQa monitoring dashboard.<br>
- AT Registry Database: Collects and stores AT metrics.<br>
- Timeseries Database: Manages time series data.<br>
- WireMQ monitoring Dashboard: Displays real-time monitoring and analytics.<br>
   

2. **OPEN API** <br>
The mATRIC APIs serve as interfaces between the platform, Access Technology applications and Orchestration applications. This process involves: <br>
- Onborading request: receiving request from relevant applications and store them in a NoSQL database creating a related profile.
- Data collection request: receiving data streams and store them in a NoSQL database.
- Service request: receiving customer service requests through the Orchestrator, complete with requirement definitions.

3. **mAT Manager**<br>
The multiple Access Technology Manager consist of monitoring Applications (mApps) that manage different xApps for each Access Technology and Orchestrator applications. <br>
- Expose monitored KPIs:
- Profiling:
- AI/ML: 
   

 
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
