FROM python:2.7.11

MAINTAINER bibi21000 <bibi21000@gmail.com>

RUN cat /etc/issue
RUN env
RUN /sbin/ip addr

RUN apt-get update && \
    apt-get install -y build-essential libwrap0-dev libc-ares-dev python-dev && \
    apt-get dist-upgrade -y && \
    apt-get install -y sudo openssh-server && \
    mkdir -p /var/run/sshd && \
    apt-get install -y sudo supervisor && \
    mkdir -p /var/log/supervisor && \
    apt-get clean && \
    rm -Rf /root/.cache/*

COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir /opt/janitoo && \
    for dir in src home log run etc init; do mkdir /opt/janitoo/$dir; done && \
    mkdir /opt/janitoo/src/janitoo

ADD . /opt/janitoo/src/janitoo

WORKDIR /opt/janitoo/src

RUN ln -s janitoo/Makefile.all Makefile && \
    make docker-deps && \
    make deps module=janitoo && \
    make develop module=janitoo && \
    apt-get clean && \
    [ -d /root/.cache ] && rm -Rf /root/.cache/*

RUN make clone module=janitoo_mosquitto && \
    make clone module=janitoo_pki && \
    apt-get clean && \
    [ -d /root/.cache ] && rm -Rf /root/.cache/*

RUN make clone module=janitoo_db && \
    make clone module=janitoo_db_full && \
    apt-get clean && \
    [ -d /root/.cache ] && rm -Rf /root/.cache/*

RUN make clone module=janitoo_layouts && \
    apt-get clean && \
    [ -d /root/.cache ] && rm -Rf /root/.cache/*

RUN make clone module=janitoo_datalog_rrd && \
    apt-get clean && \
    [ -d /root/.cache ] && rm -Rf /root/.cache/*

RUN make clone module=janitoo_flask && \
    make clone module=janitoo_flask_socketio && \
    make clone module=janitoo_manager && \
    make clone module=janitoo_manager_proxy && \
    apt-get clean && \
    [ -d /root/.cache ] && rm -Rf /root/.cache/*

VOLUME ["/etc/mosquitto/", "/var/data/mosquitto", "/var/log/mosquitto", "/opt/janitoo/home", "/opt/janitoo/log", "/opt/janitoo/etc"]

EXPOSE 22 1883 5005 9001

CMD ["/usr/bin/supervisord", "--nodaemon"]
