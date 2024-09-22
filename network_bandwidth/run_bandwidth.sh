#!/usr/bin/env bash

iperf -c "$1" -t 300 -P 3 -i 1 >> results_1.txt
sleep 240
iperf -c "$1" -t 100 -P 3 -i 1 >> results_2.txt
