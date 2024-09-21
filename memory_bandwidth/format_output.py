import json

# Function to parse the file and convert it to JSON
def parse_file_to_json(file_path):
    # Open the file and read the content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # First line: Final values
    final_values = lines[0].strip()

    # Second line: Threads times
    threads_times = lines[1].strip()

    # Parse the final values
    throughput_memory, throughput_elements, time_ns = final_values.split()

    # Remove the 'GB/s' and 'ns' suffix from the parsed values
    time_ns = float(time_ns.replace('ns', ''))
    throughput_elements = float(throughput_elements)

    # Convert thread times to a list of integers
    threads_times = list(map(int, threads_times.split()))

    # Create the JSON object
    data = {
        "throughput_memory": throughput_memory,
        "throughput_elements": throughput_elements,
        "time_ns": time_ns,
        "threads_times": threads_times
    }

    # Convert to JSON
    json_data = json.dumps(data, indent=4)

    return json_data

# Specify the path to the input file
file_path = 'input.txt'  # Replace with the path to your file

# Call the function and print the result
json_output = parse_file_to_json(file_path)
print(json_output)
