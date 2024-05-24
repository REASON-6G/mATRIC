
![Logo_updated](https://github.com/REASON-6G/mATRIC/assets/63154875/84b47223-21dc-4c86-8cb0-4f160bdd932b)


mATRIC is multi-Access Technology 
Intelligent Controller

# Basic overview 
This repository host the mATRIC software implementation platform, an intelligent RAN controller developed under the [![Static Badge](https://img.shields.io/badge/REASON-project)](https://reason-open-networks.ac.uk/about/) project to support multiple wireless access technologies.


**The mATRIC platform supports the following capabilities:**

- Real-time and near real-time scenarios.
- Cellular and non-cellular access technologies – _5G, WiFi, LiFi_.
- Monitoring, intelligence and data analytics.
- Control and optimisation of RAN resources.


# Architecture

**mATRIC platform consist of 3 key building blocks.** <br>
The platform is compatible with standard ORAN and 3GPP interfaces. The E2 and O1 interfaces provide access to the mATRIC platform, enabling it to gather metrics and interact with RAN nodes. This functionality enables the integration of multiple access technologies with the platform. <br>
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
The multiple Access Technology Manager consist of monitoring Applications (mApps) that manage xApps for each AT application. <br>
- Expose monitored KPIs: Extracts data for exposure from different access technology.
- Profiling: Performs profiling functions.
 
   

 
![alt text](/matric.png)

# Deployment of mATRIC

Follow these steps to build and run the key containers of mATRIC using Docker Compose. <br>

1.	Clone this repository.
2.	Build and run the key containers of mATRIC using Docker Compose.
Open a terminal and run the following command in the directory where your docker-compose.yml is located:

  	``` Bash
	docker-compose build
	```
This command builds all the containers specified in your docker-compose.yml file.

3.	Start the containers by using the following command:
   
	``` Bash
	docker-compose up
	```
This will start all the services defined in your docker-compose.yml file. Below is a list of the key services that will be initiated:


-	emulate5g
-	emulatewifi
-	emulatelifi
-	accessaggregator
-	access5G
-	accessWifi


**Customise configuration** <br>
If you want to run a specific configuration of mATRIC, you will need to modify the docker-compose.yml file accordingly. 

# InfluxDB Configuration

Here are steps to configure InfluxDB for use with the mATRIC platform. <br>

1.	**Configuration File Settings** <br>
   Modify the `config/influxdb_config.yml` file to match your deployment settings:

   ```yaml
   [matricconfig]
   url = http://localhost:9999
   org = "UoB"
  ```

2.   **Environment Variables** <br>
    Set the environment variables in `monitoring/dbconfig.env` to configure the initial setup for InfluxDB: <br>
    
   ```
   DOCKER_INFLUXDB_INIT_MODE=setup
   DOCKER_INFLUXDB_INIT_USERNAME=matricAdmin
   DOCKER_INFLUXDB_INIT_PASSWORD=your-password
   DOCKER_INFLUXDB_INIT_ORG=UoB
   DOCKER_INFLUXDB_INIT_BUCKET=DefaultBucket
   DOCKER_INFLUXDB_INIT_ADMIN_TOKEN= your-admin-token
   INFLUXDB_DB=matricDB
   INFLUXDB_USER=matricAdmin
  ```

3.    **Initialize Database** <br>
Run the script to set up your InfluxDB database: <br>

   ```
   ./scripts/init_db.sh
  ```
	
4.	**Verify Configuration** <br>
Confirm that InfluxDB is configured correctly. Run the following command to fetch a list of databases: <br>

   ```
   influx -execute 'SHOW DATABASES'
   ```

# Access Point Integration

This describes how to integrate the APs to the mATRIC platform.<br>
...



# Database Query Example

# mATRIC usage documentation

# API for Access Point Integration

This API endpoint provides mATRIC users to integrate their access points with the platform. The below guidance will assist with steps for integrating one or many access points with mATRIC.

# API for Data Access

# API for RAN Control

# How to contribute

# Licence

**MIT License**

Copyright (c) 2024 SMART INTERNET LAB

