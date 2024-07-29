import sys
import re
import json

def extract_round_trip_time(file_path):
    pattern = r'^Round-trip time: (\d+\.\d+) ms$'

    round_trip_time = []
    client_or_server = None


    with open(file_path, 'r') as file:
        client_or_server = file.readline().strip()
        for line in file:
            match = re.match(pattern, line.strip())
            if match:
                round_trip_time.append(float(match.group(1)))

    if client_or_server == 'Client':
        result = {
            f"firstRoundTrip{client_or_server}": round_trip_time[0],
            f"listRoundTrip{client_or_server}": round_trip_time[1:],
            "customXValues": [1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1]
        }
    else:
        result = {
            f"firstRoundTrip{client_or_server}": round_trip_time[0],
            f"listRoundTrip{client_or_server}": round_trip_time[1:],
        }

    json_output = json.dumps(result, indent=4)
    print(json_output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python format_output.py <file_path>")
    else:
        file_path = sys.argv[1]
        extract_round_trip_time(file_path)

