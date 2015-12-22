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
    apt-get install -y build-essential libwrap0-dev libc-ares-dev python2.7-dev git vim-nox && \
    apt-get dist-upgrade -y && \
    apt-get install -y sudo openssh-server && \
    mkdir -p /var/run/sshd && \
    sed -i -e "s/^PermitRootLogin without-password/#PermitRootLogin without-password/" /etc/ssh/sshd_config && \
    apt-get install -y sudo supervisor && \
    mkdir -p /var/log/supervisor /etc/supervisord && \
    apt-get clean && \
    rm -Rf /root/.cache/*

RUN mkdir /opt/janitoo && \
    for dir in src home log run etc/janitoo init; do mkdir /opt/janitoo/$dir; done && \
    mkdir /opt/janitoo/src/janitoo

ADD . /opt/janitoo/src/janitoo

COPY docker/auto.sh /root/
COPY docker/shell.sh /root/
COPY docker/supervisord.conf /etc/supervisord/
COPY docker/supervisord.conf.d /etc/supervisord/

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
    apt-get clean && \
    rm -Rf /root/.cache/* 2>/dev/null|| true && \
    rm -Rf /tmp/* 2>/dev/null|| true

RUN make clone module=janitoo_flask && \
    make clone module=janitoo_flask_socketio && \
    make clone module=janitoo_manager && \
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
