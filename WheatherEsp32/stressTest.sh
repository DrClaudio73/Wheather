#!/bin/bash
for ((k=1;k<=100;k++))
do
    echo -n "caio" | nc 192.168.4.1 80 -w 30
    echo $k
done