import sys
import re
import json

def extract_round_trip_time(file_path):
    pattern = r'^Round-trip time: (\d+\.\d+) ms$'
    round_trip_time = None
    client_or_server = None


    with open(file_path, 'r') as file:
        client_or_server = file.readline().strip()
        for line in file:
            match = re.match(pattern, line.strip())
            if match:
                round_trip_time = float(match.group(1))
                break

    result = {f"{client_or_server}_round_trip_time_ms": round_trip_time} if round_trip_time is not None else {}

    json_output = json.dumps(result, indent=4)
    print(json_output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python format_output.py <file_path>")
    else:
        file_path = sys.argv[1]
        extract_round_trip_time(file_path)

