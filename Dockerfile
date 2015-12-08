FROM python:2.7.10
MAINTAINER bibi21000 <bibi21000@gmail.com>
RUN mkdir /opt/janitoo
RUN for dir in src home log run etc init; do mkdir /opt/janitoo/$dir; done
RUN mkdir /opt/janitoo/src/janitoo
ADD . /opt/janitoo/src/janitoo
WORKDIR /opt/janitoo/src
RUN ln -s janitoo/makefile.all Makefile
RUN ls -lisa
RUN ls -lisa janitoo
RUN make deps module=janitoo
RUN make develop module=janitoo

RUN make pull module=janitoo_db
RUN make deps module=janitoo_db
RUN make develop module=janitoo_db

RUN make pull module=janitoo_db_full
RUN make deps module=janitoo_db_full
RUN make develop module=janitoo_db_full

RUN make tests-all
