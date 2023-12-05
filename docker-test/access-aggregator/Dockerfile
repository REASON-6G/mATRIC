FROM ubuntu:22.04

# Updates
RUN apt-get update -y

# Install Python 3.10
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt install python3.10 pip python3.10-venv -y
RUN pip install influxdb-client

# Install other dependencies
RUN apt install wget curl mariadb-server-10.6 sqlite3 -y

# Install MariaDB C connector
RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup \ --mariadb-server-version="mariadb-10.6"
RUN apt install libmariadb3 libmariadb-dev -y


# Install wiremq
RUN mkdir /wiremq
WORKDIR /wiremq
COPY bin/wiremq-0.0.1-py3-none-any.whl .
COPY bin/requirements.txt .
COPY bin/Makefile .
RUN make requirements
RUN make directories
RUN make build

# Install mATRIC application
COPY access-aggregator/app ./app

# Run the python application
ENTRYPOINT ["python3", "/wiremq/app/main.py"]
