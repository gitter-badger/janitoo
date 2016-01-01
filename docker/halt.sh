#!/bin/bash
echo "Halting ..."
killall supervisord
echo "Waiting for shutdown for 10 seconds ..."
sleep 10
ps aux
echo "Waiting for shutdown for 10 seconds ..."
sleep 10
ps aux
echo "Waiting for shutdown for 5 seconds ..."
sleep 5
ps aux
echo "Waiting for shutdown for 5 seconds ..."
sleep 5
ps aux
echo "Killing main process ..."
killall python 2>/dev/null
