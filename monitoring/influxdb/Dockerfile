FROM influxdb:latest

COPY influxdb/createBuckets.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/createBuckets.sh

 