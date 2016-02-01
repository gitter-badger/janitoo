.. image:: https://travis-ci.org/bibi21000/janitoo.svg?branch=master
    :target: https://travis-ci.org/bibi21000/janitoo
    :alt: Travis status

.. image:: https://circleci.com/gh/bibi21000/janitoo.png?style=shield
    :target: https://circleci.com/gh/bibi21000/janitoo
    :alt: Circle status

.. image:: https://coveralls.io/repos/bibi21000/janitoo/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/bibi21000/janitoo?branch=master
    :alt: Coveralls results

.. image:: https://img.shields.io/imagelayers/image-size/bibi21000/janitoo_base/latest.svg
    :target: https://hub.docker.com/r/bibi21000/janitoo_base/
    :alt: Docker size

.. image:: https://img.shields.io/imagelayers/layers/bibi21000/janitoo_base/latest.svg
    :target: https://hub.docker.com/r/bibi21000/janitoo_base/
    :alt: Docker size

==================
Welcome to Janitoo
==================

Not another Home Automation software ... a full protocol

First of all, Janito is in its eraly stages. So it is just for developers.

A video of presentation is available on youtube : https://www.youtube.com/watch?v=S3Gqj32sJ-Q

This file will be published on your github account

What is Janitoo
===============

Controllers, nodes and values
-----------------------------

Networks controllers maintains a "map" of the network.
There are of 2 types : primaries and secondaries.

The primary will serve configuration parameters for the nodes.

The network is managed by a finish state machine. Only the fail mode can be considered as usuable.

A node holds values.

There is many genres of values :
 - system : needed by the protocol itself.
 - config : used to configure nodes and values
 - basic : base values. Used by nodes themselves and andvanced users.
 - user : for common users
 - command : to launch advanced commands ie pairing

Examples of nodes/values

- an ups is a node (janitoo_nut). battery_level, upsstate, ... are values
- a vacuum is a node (janitoo_roomba). baterry_level, dock state but also clean, dock commands are values
- an rrd source is a node
- an arduino is a node

...

If your familiar with openzwave and the zwave protocol, janitoo is a king of zwave over mqtt.

Multi_hardware
--------------
Due to its low memory footprint, janitoo can be used on many hardwares :

- Arduino mega. Actually, it's impossible to install it on an Uno.
- Raspberry : the 0 will be supported (python). The janitoo_hostsensor with 7 nodes and about 100 values only takes 3% of memory and 7% of cpu on a Raspberry B.

...

Deploying Janitoo
=================
Choose yours hosts
------------------

 - mqtt server
 - mysql server or sqlite
  ...

Mosquitto
---------

This is the mqtt server.

..code: bash

    sudo apt-get install mosquitto


By default, it will listen on all interfaces. Auth is actually not fully implmented.

On every computers
------------------

Create a directory for janitoo. It is highly recommended to put it in /opt/janitoo.

..code: bash

    sudo mkdir /opt/janitoo

    sudo chown me:me /opt/janitoo

    cd /opt/janitoo

    for dir in src home log run etc init; do
        mkdir $dir
    done


Go to the src directory :

..code: bash

    cd src


Clone janitoo repository from github

..code: bash

    git clone https://github.com/bibi21000/janitoo.git


Create a link to the makefile helper:

..code: bash

    ln -s janitoo/makefile.all Makefile


You can now "develop" janitoo. It use a lot of entry-points, so it MUST be developed:

..code: bash

    make develop module=janitoo

Installing mosquito
-------------------

..code: bash

    make clone module=janitoo_mosquitto

Installing suplementary modules
-------------------------------

You are now ready to install modules. You don't need to install all of them on the same host.

For example, if you want to monitor cpu speed and voltage on a raspberry, you must install :

..code: bash

    make clone module=janitoo_hostsensor_raspberry


Your admin password may be asked by sudo. Sometimes, it's necessary to install debian (or unduntu) dependencies.

If you want to monitor disks and processes, you can install the extension:

..code: bash

    make clone module=janitoo_hostsensor_psutil

On a laptop, you can use the lmsensor extension:

..code: bash

    make clone module=janitoo_hostsensor_lmsensor

You can now create you init script :

..code: bash

    cd /opt/janitoo/init

    vim jnt_hostsensor.sh

        #!/bin/bash
        JNT_HOME=/opt/janitoo/src
        SVC_NAME=raspberry

        cd ${JNT_HOME}/janitoo_${SVC_NAME}/src/scripts/ && ./jnt_${SVC_NAME} -c ${JNT_HOME}/janitoo_${SVC_NAME}/src/config/janitoo_${SVC_NAME}.conf $*

And your

    ln -s /opt/janitoo/src/janitoo_hostsensor/script

Actually, the protocol is not fully developped, so you must create nodes in your configuration files.


Support
=======

You can ask about support to google the google group : https://groups.google.com/d/forum/janitoo-dev

