import json
import sys

def parse_file_to_json(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    throughput_memory_list = []
    throughput_elements_list = []
    time_list = []
    threads_list = []
    thread_count_list = []
    for i in range(0, len(lines), 2):
        final_values = lines[0].strip()
        threads_times = lines[1].strip()

        _, throughput_memory, throughput_elements, time_ns = final_values.split()

        throughput_memory = float(throughput_memory.replace('GB/s', ''))
        throughput_elements = float(throughput_elements)
        time_ns = float(time_ns.replace('ns', ''))

        threads_times = list(map(int, threads_times.split()))

        throughput_memory_list.append(throughput_memory)
        throughput_elements_list.append(throughput_elements)
        time_list.append(time_ns)
        threads_list.append(threads_times)
        thread_count_list.append(len(threads_times))

    data = {
        "thread_counts": thread_count_list,
        "throughput_memory_gb_s": throughput_memory_list,
        "throughput_elements": throughput_elements_list,
        "time_ns": time_list,
        "threads_times": threads_list
    }
    json_output = json.dumps(data, indent=4)
    print(json_output)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python format_output.py <file_path>")
    else:
        file_path = sys.argv[1]
        parse_file_to_json(file_path)

