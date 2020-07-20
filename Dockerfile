FROM ubuntu:bionic

RUN \
 apt-get update --fix-missing \
 && apt-get install -y -q curl gnupg \
 && curl -sSL 'http://p80.pool.sks-keyservers.net/pks/lookup?op=get&search=0x8AA7AF1F1091A5FD' | apt-key add -  \
 && echo 'deb [arch=amd64] http://repo.sawtooth.me/ubuntu/chime/stable bionic universe' >> /etc/apt/sources.list \
 && apt-get update --fix-missing

RUN apt-get install -y --allow-unauthenticated -q \
    curl \
    python3-pip

RUN pip3 install \
    aiohttp \
    jinja2 \
    aiohttp_jinja2 \
    aiohttp_session \
    pymongo

WORKDIR /project/chat-room

ENV PATH $PATH:/project/chat-room/bin