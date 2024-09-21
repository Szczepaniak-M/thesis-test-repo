#!/bin/bash

experiments=("write" "randwrite" "read" "randread" "randrw")
for exp in "${experiments[@]}"
do
    output_file="results-${exp}-node.json"
    sudo fio --name=noisy --rw="${exp}" --numjobs=4 --refill_buffers --ioengine=libaio --time_based --runtime=60s --group_reporting --iodepth=128 --bs=4k --filename=/dev/nvme0n1 --size=20G --direct=1 --output-format=json,terse --output="$output_file"
done
