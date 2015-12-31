#!/bin/bash
echo "Halting ..."
killall supervisord
echo "Sleeping 5 seconds ..."
sleep 5
ps aux
echo "Sleeping 5 seconds ..."
sleep 5
ps aux
echo "Sleeping 5 seconds ..."
sleep 5
ps aux
echo "Sleeping 5 seconds ..."
sleep 5
ps aux
echo "Killing main process ..."
killall python
