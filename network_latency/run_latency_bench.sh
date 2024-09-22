#!/usr/bin/env sh

./sockperf ping-pong -i node-2 -t 1100 --full-log logs.csv --full-rtt --tcp >> results.txt