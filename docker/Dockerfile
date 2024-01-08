FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3.12-distutils \
    python3.12-full \
    git

RUN python3.12 -m ensurepip --upgrade && \
    python3.12 -m pip install --upgrade pip && \
    python3.12 -m pip install \
    poetry

WORKDIR /opt

RUN git clone https://github.com/gembcior/TakeMe.git && \
    cd TakeMe && \
    mkdir instance && \
    poetry install

WORKDIR /opt/TakeMe

CMD poetry run gunicorn --worker-class eventlet -w 1 --threads 100 takeme.run:app -b 0.0.0.0
