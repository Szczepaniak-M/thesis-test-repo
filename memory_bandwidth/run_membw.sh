#!/usr/bin/env bash

echo "threads,bw,sum" > results.csv
threads=(1 2 4 6 8 12 16 18 20 22 24 28 32 36 40 44 48) 
# fill 75% of RAM size with uint64_t
size_kb=$(free -b | grep Mem: | awk '{print $2}')
input_size=$(echo "$size_kb * 0.75 / 8" | bc)

for t_count in "${threads[@]}";
do
  numactl --cpubind=0 --membind=0 -- ./membw $input_size $t_count 50 >> results.csv
done
