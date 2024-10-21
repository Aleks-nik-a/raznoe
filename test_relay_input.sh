#!/bin/bash

trap "echo ' Pressed Ctrl-C, send OFF command ' && modbus_client -mrtu  --debug /dev/ttyRS485-2 -s2 -pnone -a1 -t5 -r 0x003 0 > /dev/null && echo 'starting wb-mqtt-serial' && service wb-mqtt-serial start && exit" SIGINT

echo 'Stoping wb-mqtt-serial'
service wb-mqtt-serial stop

while true
do
modbus_client -mrtu  --debug /dev/ttyRS485-2 -s2 -pnone -a1 -t5 -r 0x003 1 > /dev/null
if [ $? -eq 0 ]; then
echo relay ON - OK
else
echo relay ON - FAIL
break
fi

sleep 1

modbus_client -mrtu  --debug /dev/ttyRS485-2 -s2 -pnone -a1 -t5 -r 0x003 0 > /dev/null
if [ $? -eq 0 ]; then
echo relay OFF - OK
else
echo relay OFF - FAIL
break
fi

sleep 1


done