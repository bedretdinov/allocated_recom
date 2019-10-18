FROM python:3.6-jessie

LABEL maintainer="RPyCServer Classic"

WORKDIR /app
#VOLUME
COPY  . /app

# expect a build-time variable
RUN sed -i '/jessie-updates/d' /etc/apt/sources.list \
&&   apt-get update  \
&&   apt-get install -y \
&&   apt-get -y install vim \
&&   apt-get -y install python3-pip \
&&   pip3 install --upgrade pip \
&&   pip3 install rpyc

RUN /usr/local/bin/rpyc_classic.py --port=8000