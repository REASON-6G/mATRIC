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

1.	Configuration file settings <br>
Navigate to monitoring/influxdb/config.yml

``` YAML 
[matricconfig]
url = http://localhost:9999
token = ""XAyfr1nVMvW0eStmjIbJJzDIaC0rPt40wZiIlqy8yoauVp5V1mb_ZT1gLJX3ujrKJl64RZvsV4teq3iyw2UFfQ==""
org = "UoB"

```



2.	Environment variables

Set the environment variables in monitoring/dbconfig.env to configure the initial setup for InfluxDB: 

``` env

DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=matricAdmin
DOCKER_INFLUXDB_INIT_PASSWORD=your-password
DOCKER_INFLUXDB_INIT_ORG=UoB
DOCKER_INFLUXDB_INIT_BUCKET=DefaultBucket
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN= XAyfr1nVMvW0eStmjIbJJzDIaC0rPt40wZiIlqy8yoauVp5V1mb_ZT1gLJX3ujrKJl64RZvsV4teq3iyw2UFfQ…
INFLUXDB_DB=matricDB
INFLUXDB_USER=matricAdmin

```


3.	Docker Compose setup
InfluxDB is cconfigured to run as Docker container.  Check the monitoring/docker-compose.yml for service configuration:

	```YAML
	influxdb:
	  image: influxdb:latest
	  env_file:
	    - dbconfig.env
	```



# Access Point Integration

# Database Query Example

# mATRIC usage documentation

# API for Access Point Integration

This API endpoint provides mATRIC users to integrate their access points with the platform. The below guidance will assist with steps for integrating one or many access points with mATRIC.

# API for Data Access

# API for RAN Control

# How to contribute
