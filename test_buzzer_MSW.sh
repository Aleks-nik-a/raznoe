#!/bin/bash

trap "echo ' Pressed Ctrl-C, send buzzer OFF command ' && modbus_client -mrtu  --debug /dev/ttyRS485-2 -s2 -pnone -a108 -t5 -r 0x0000 0  && exit" SIGINT

while true
do
modbus_client -mrtu  --debug /dev/ttyRS485-2 -s2 -pnone -a108 -t5 -r 0x0000 1 > /dev/null
if [ $? -eq 0 ]; then
echo Buzzer ON - OK
else
echo Buzzer ON - FAIL
break
fi

sleep 1

modbus_client -mrtu  --debug /dev/ttyRS485-2 -s2 -pnone -a108 -t5 -r 0x0000 0 > /dev/null
if [ $? -eq 0 ]; then
echo Buzzer OFF - OK
else
echo Buzzer OFF - FAIL
break
fi

sleep 1


done