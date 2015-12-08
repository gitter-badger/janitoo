FROM python:2.7.10

MAINTAINER bibi21000 <bibi21000@gmail.com>

RUN apt-get update
RUN apt-get install -y build-essential libssl-dev libwrap0-dev libc-ares-dev python-dev
RUN apt-get -y install libevent-2.0-5 mosquitto sudo

RUN mkdir /opt/janitoo
RUN for dir in src home log run etc init; do mkdir /opt/janitoo/$dir; done
RUN mkdir /opt/janitoo/src/janitoo
ADD . /opt/janitoo/src/janitoo

WORKDIR /opt/janitoo/src
RUN ln -s janitoo/Makefile.all Makefile

RUN make docker-deps

RUN make deps module=janitoo
RUN make develop module=janitoo

RUN make clone module=janitoo_db

RUN make clone module=janitoo_db_full

RUN make tests-all

VOLUME ["/etc/mosquitto/", "/var/data/mosquitto", "/var/log/mosquitto", "/opt/janitoo"]

EXPOSE 1883 8883
