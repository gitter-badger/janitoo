FROM python:2.7.10

MAINTAINER bibi21000 <bibi21000@gmail.com>

RUN env
RUN /sbin/ip addr

RUN apt-get update
RUN apt-get install -y build-essential libssl-dev libwrap0-dev libc-ares-dev python-dev
RUN apt-get install -y libevent-2.0-5 mosquitto sudo
RUN apt-get install -y netcat-openbsd

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

RUN make clone module=janitoo_layouts

RUN make clone module=janitoo_hostsensor
RUN make clone module=janitoo_hostsensor_psutil
RUN make clone module=janitoo_hostsensor_lmsensor

RUN make clone module=janitoo_nut

RUN make clone module=janitoo_datalog_rrd

RUN make clone module=janitoo_flask
RUN make clone module=janitoo_manager
RUN make clone module=janitoo_manager_proxy

RUN cat /etc/mosquitto/mosquitto.conf
RUN ls -lisa /etc/mosquitto/conf.d/
RUN netcat -zv 127.0.0.1 1-9999

RUN service mosquitto restart

RUN make tests-all

VOLUME ["/etc/mosquitto/", "/var/data/mosquitto", "/var/log/mosquitto", "/opt/janitoo"]

#EXPOSE 1883 8883