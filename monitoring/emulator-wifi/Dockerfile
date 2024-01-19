FROM python:3.10

WORKDIR /usr/app/src

COPY emulator-wifi/app/ ./
COPY ./bin/baseapemulator.py ./

CMD ["python", "emulate-wifi.py"]