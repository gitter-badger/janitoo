FROM python:2.7

MAINTAINER bibi21000 <bibi21000@gmail.com>

RUN cat /etc/issue
RUN env
RUN /sbin/ip addr

COPY docker/auto.sh /root/
COPY docker/shell.sh /root/
COPY docker/supervisord.conf /root/
COPY docker/supervisord.conf.d /root/

RUN echo "janitoo\njanitoo" | passwd

RUN apt-get update && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN apt-get install -y build-essential libwrap0-dev libc-ares-dev python2.7-dev git vim-nox && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN apt-get install -y sudo cron openssh-server lsb-release lsb-base && \
    mkdir -p /var/run/sshd && \
    sed -i -e "s/^PermitRootLogin without-password/#PermitRootLogin without-password/" /etc/ssh/sshd_config && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN apt-get install -y sudo supervisor && \
    mkdir -p /var/log/supervisor /etc/supervisord && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN mkdir /opt/janitoo && \
    for dir in src cache cache/janitoo_manager home log run etc init; do mkdir /opt/janitoo/$dir; done && \
    mkdir /opt/janitoo/src/janitoo

ADD . /opt/janitoo/src/janitoo

COPY docker/auto.sh /root/
COPY docker/shell.sh /root/
COPY docker/rescue.sh /root/
COPY docker/supervisord-tests.conf /etc/supervisord/
COPY docker/supervisord-tests.conf.d/ /etc/supervisord/supervisord-tests.conf.d/
COPY docker/supervisord.conf /etc/supervisord/
COPY docker/supervisord.conf.d/ /etc/supervisord/supervisord.conf.d/

WORKDIR /opt/janitoo/src

RUN ln -s janitoo/Makefile.all Makefile && \
    make docker-deps && \
    make deps module=janitoo && \
    make develop module=janitoo && \
    make clone module=janitoo_nosetests && \
    make clone module=janitoo_nosetests_flask && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN make clone module=janitoo_pki && \
    make clone module=janitoo_nginx && \
    make clone module=janitoo_mosquitto && \
    apt-get clean && \
    mkdir -p /var/log/gunicorn || true && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN make clone module=janitoo_db && \
    make clone module=janitoo_db_full && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN make clone module=janitoo_layouts && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN make clone module=janitoo_datalog_rrd && \
    cp janitoo_datalog_rrd/src/config/janitoo_datalog_rrd.conf /opt/janitoo/etc/ &&\
    cp janitoo_datalog_rrd/src/scripts/supervisord.conf /etc/supervisord/supervisord.conf.d/ &&\
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN make clone module=janitoo_flask && \
    make clone module=janitoo_flask_socketio && \
    make clone module=janitoo_manager && \
    install -m 0644 janitoo_manager/src/config/janitoo_manager.conf /opt/janitoo/etc/janitoo_manager.conf &&\
    install -m 0644 janitoo_manager/src/config/janitoo_manager.nginx.conf /etc/nginx/conf.d/janitoo_manager &&\
    install -m 0644 janitoo_manager/src/config/janitoo_manager.gunincorn.conf /etc/gunicorn.d/janitoo_manager.conf &&\
    make clone module=janitoo_manager_proxy && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN apt-get install -y python-pip lm-sensors && \
    pip install psutil bottle batinfo https://bitbucket.org/gleb_zhulik/py3sensors/get/tip.tar.gz && \
    cd /root/ && \
    git clone -b develop https://github.com/nicolargo/glances.git && \
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

VOLUME ["/etc/nginx/conf.d/", "/var/log/nginx", "/etc/mosquitto/", "/var/data/mosquitto", "/var/log/mosquitto", "/var/log/supervisor", "/opt/janitoo/home", "/opt/janitoo/log", "/opt/janitoo/etc"]

EXPOSE 22 1883 5005 8085 9001

CMD ["/root/auto.sh"]
