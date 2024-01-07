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

RUN python3.12 -m ensurepip --upgrade

RUN python3.12 -m pip install --upgrade setuptools && \
    python3.12 -m pip install --upgrade pip

RUN python3.12 -m pip install \
    poetry \
    eventlet \
    gunicorn

WORKDIR /opt

RUN git clone https://github.com/gembcior/TakeMe.git && \
    poetry config virtualenvs.create false && \
    cd TakeMe && \
    poetry install

CMD gunicorn --worker-class eventlet -w 1 --threads 100 takeme.run:app -b 0.0.0.0
