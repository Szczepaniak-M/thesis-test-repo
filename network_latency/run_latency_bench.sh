#!/usr/bin/env sh

./sockperf/sockperf ping-pong -i node-2 -t 60 --full-log logs.csv --full-rtt --tcp >> results.txt