FROM python:2.7.10

MAINTAINER bibi21000 <bibi21000@gmail.com>

RUN env
RUN /sbin/ip addr

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libwrap0-dev libc-ares-dev python-dev && \
    apt-get install -y sudo openssh-server && \
    mkdir -p /var/run/sshd && \
    apt-get install -y sudo supervisor && \
    mkdir -p /var/log/supervisor && \
    apt-get install -y mosquitto

ADD docker/supervisord.conf /etc/supervisor/conf.d/

RUN mkdir /opt/janitoo && \
    for dir in src home log run etc init; do mkdir /opt/janitoo/$dir; done && \
    mkdir /opt/janitoo/src/janitoo
ADD . /opt/janitoo/src/janitoo

WORKDIR /opt/janitoo/src
RUN ln -s janitoo/Makefile.all Makefile && \
    make docker-deps && \
    make deps module=janitoo && \
    make develop module=janitoo

RUN make clone module=janitoo_db && \
    make clone module=janitoo_db_full

RUN make clone module=janitoo_layouts

RUN make clone module=janitoo_hostsensor && \
    make clone module=janitoo_hostsensor_psutil && \
    make clone module=janitoo_hostsensor_lmsensor

RUN make clone module=janitoo_nut

RUN make clone module=janitoo_datalog_rrd

RUN make clone module=janitoo_flask && \
    make clone module=janitoo_manager && \
    make clone module=janitoo_manager_proxy

RUN /usr/bin/supervisord && make tests-all

VOLUME ["/etc/mosquitto/", "/var/data/mosquitto", "/var/log/mosquitto", "/opt/janitoo"]

EXPOSE 22 1883

CMD ["/usr/bin/supervisord"]
