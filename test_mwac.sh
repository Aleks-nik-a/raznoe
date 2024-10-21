#!/bin/bash


if [ -n "$1" ]
then
ADDRESS=$1
echo "используется адрес ${ADDRESS}"
else
echo "используется широковещательный адрес 0"
ADDRESS=0
fi


set -x

#echo 'Stoping wb-mqtt-serial and wb-mqtt-gpio...'
#service wb-mqtt-serial stop
#service wb-mqtt-gpio stop
echo 'Включаем питаеие и ждём 3 секунды'
gpioset $(gpiofind "MOD3 RTS")=1 # включаем питание
sleep 3

echo 'перезагружаем модуль'
gpioset $(gpiofind "MOD3 RTS")=0
sleep 0.1
gpioset $(gpiofind "MOD3 RTS")=1

echo "считываем реристр 330 по адресу ${ADDRESS}  2 раза для проверки, что устройство в бутлоадере (-c7 не должно прочитаться)"
#modbus_client -mrtu -pnone -s2 /dev/ttyRS485-2 -b115200  -t0x3 -a $ADDRESS -r 330 -c8
#modbus_client -mrtu -pnone -s2 /dev/ttyRS485-2 -b115200  -t0x3 -a $ADDRESS -r 330 -c7
sleep 0.05 #аналог запроса на скорости 115200
modbus_client -mrtu -pnone -s2 /dev/ttyRS485-2 -b9600  -t0x3 -a $ADDRESS -r 330 -c8
modbus_client -mrtu -pnone -s2 /dev/ttyRS485-2 -b9600  -t0x3 -a $ADDRESS -r 330 -c7


#echo 'запускаем сервисы mqtt и gpio'
#service wb-mqtt-gpio start && service wb-mqtt-serial start
