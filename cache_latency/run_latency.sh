#!/usr/bin/env bash

threads=(1 2 4 6 8 12 16 18 20 22 24 28 32 36 40 44 48)
input_size=1000000 # ask for value
ool=100000         # ask for value
repeat=10          # ask for value
for t_count in "${threads[@]}";
do
  ./latency $t_count $input_size $repeat $ool >> results.txt
done
