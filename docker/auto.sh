#!/bin/bash
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
cd /root/glances
git pull origin develop
#You must loop here
python -m glances
