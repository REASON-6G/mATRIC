FROM python:3.10

WORKDIR /usr/app/src

COPY emulator-5g/app/ ./
COPY ./bin/baseapemulator.py ./

CMD ["python", "emulate-5g.py"]