#!/bin/bash
/usr/bin/supervisord -c /etc/supervisord/supervisord.conf
#You must loop here
/bin/bash
