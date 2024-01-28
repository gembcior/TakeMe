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
    poetry build

RUN pip install --ignore-installed TakeMe/dist/*.whl && \
    mkdir -p /usr/var/takeme-instance

WORKDIR /usr/var/takeme-instance

RUN echo "BCRYPT_LOG_ROUNDS = 12" >> application.cfg && \
    echo "CSRF_ENABLED = True" >> application.cfg && \
    echo "DEBUG = False" >> application.cfg && \
    echo "DEVELOPMENT = False" >> application.cfg && \
    echo "SQLALCHEMY_TRACK_MODIFICATIONS = True" >> application.cfg && \
    echo "WTF_CSRF_ENABLED = True" >> application.cfg && \
    echo "SECRET_KEY = '$(python3.12 -c 'import secrets; print(secrets.token_hex())')'" >> application.cfg

CMD gunicorn --worker-class eventlet -w 1 --threads 100 takeme.run:app -b 0.0.0.0
