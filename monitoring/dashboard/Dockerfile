FROM python:3.9
LABEL MAINTAINER Digital Catapult

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app


COPY dashboard/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install waitress


COPY dashboard .
EXPOSE 5000
CMD ["./entrypoint.sh"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
