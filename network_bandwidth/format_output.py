import re
import sys
import json
from collections import defaultdict

def parse_iperf(file_path, suffix):
    connection_bandwidths = defaultdict(lambda: defaultdict(float))
    sum_bandwidth = defaultdict(float)
    min_bandwidth = defaultdict(float)
    max_bandwidth = defaultdict(float)
    avg_bandwidth = defaultdict(float)
    intervals = set()

    connection_pattern = re.compile(r'\[\s*(\d+)\]\s+([\d.]+)-([\d.]+)\s+sec\s+([\d.]+)\s+GBytes\s+([\d.]+)\s+Gbits/sec')
    sum_pattern = re.compile(r'\[SUM\]\s+([\d.]+)-([\d.]+)\s+sec\s+([\d.]+)\s+GBytes\s+([\d.]+)\s+Gbits/sec')

    with open(file_path, 'r') as f:
        for line in f:
            connection_match = connection_pattern.search(line)
            if connection_match:
                connection_id = int(connection_match.group(1))
                start_time = float(connection_match.group(2))
                bandwidth = float(connection_match.group(5))

                connection_bandwidths[connection_id][start_time] = bandwidth
                intervals.add(start_time)

            sum_match = sum_pattern.search(line)
            if sum_match:
                start_time = float(sum_match.group(1))
                bandwidth_sum = float(sum_match.group(4))

                sum_bandwidth[start_time] = bandwidth_sum
                intervals.add(start_time)
    if not sum_bandwidth:
        sum_bandwidth = connection_bandwidths[1]
    intervals = sorted(intervals)
    for i in intervals:
        interval = []
        for j in range(1, len(connection_bandwidths) + 1):
            interval.append(connection_bandwidths[j][i])
        min_bandwidth[i] = min(interval)
        max_bandwidth[i] = max(interval)
        avg_bandwidth[i] = sum(interval) / len(interval)

    data = {
        f'intervals_{suffix}': intervals,
        f'connection_min_{suffix}': [min_bandwidth.get(i, 0) for i in intervals],
        f'connection_max_{suffix}': [max_bandwidth.get(i, 0) for i in intervals],
        f'connection_avg_{suffix}': [avg_bandwidth.get(i, 0) for i in intervals],
        f'sum_bandwidth_{suffix}': [sum_bandwidth.get(i, 0) for i in intervals]
    }

    return data

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python format_output.py <input_file_1> <input_file_2>")
        sys.exit(1)

    file_path_1 = sys.argv[1]
    data_1 = parse_iperf(file_path_1, 'first_attempt')

    file_path_2 = sys.argv[2]
    data_2 = parse_iperf(file_path_2, 'second_attempt')

    # Output the JSON data
    merged_dict = data_1 | data_2
    print(json.dumps(merged_dict, indent=4))
