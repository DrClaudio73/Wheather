#!/bin/bash
for ((k=1;k<=100;k++))
do
     echo -n -e "GET /clean_csv HTTP/1.1\r\n\r\n" | nc 192.168.1.104 80 -w 60
    echo $k
done