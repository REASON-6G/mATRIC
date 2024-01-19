FROM python:3.10

WORKDIR /usr/app/src

COPY emulator-lifi/app/ ./
COPY ./bin/baseapemulator.py ./

CMD ["python", "emulate-lifi.py"]