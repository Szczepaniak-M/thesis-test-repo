import re
import json
import sys

def parse_results(file_path):
    metrics = {
        'avg_latency_us': None,
        'min_latency_us': None,
        'max_latency_us': None,
        'percentile_99_us': None
    }

    avg_pattern = re.compile(r'Avg Latency:\s+([\d\.]+)\s+usec')
    min_pattern = re.compile(r'Min Latency:\s+([\d\.]+)\s+usec')
    max_pattern = re.compile(r'Max Latency:\s+([\d\.]+)\s+usec')
    percentile_99_pattern = re.compile(r'99th Percentile Latency:\s+([\d\.]+)\s+usec')

    with open(file_path, 'r') as f:
        for line in f:
            if avg_match := avg_pattern.search(line):
                metrics['avg_latency_us'] = float(avg_match.group(1))
            if min_match := min_pattern.search(line):
                metrics['min_latency_us'] = float(min_match.group(1))
            if max_match := max_pattern.search(line):
                metrics['max_latency_us'] = float(max_match.group(1))
            if p99_match := percentile_99_pattern.search(line):
                metrics['percentile_99_us'] = float(p99_match.group(1))

    print(json.dumps(metrics, indent=4))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_results.py <results.txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    parse_results(file_path)
