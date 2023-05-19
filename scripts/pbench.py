import sys
import time
import subprocess
import numpy as np
import argparse

def run_benchmark(binary_file, n):
    times = []
    for i in range(n):
        if 'XML' in binary_file:
            output=str(subprocess.check_output([binary_file, "./XML/standart.xml"]))
            times.append(int(output.split("Total time=", 1)[1][:-3]))
        else:
            start_time = time.time()
            subprocess.run(binary_file)
            end_time = time.time()
            times.append(end_time - start_time)
    return times

def calculate_stats(times):
    total_time = sum(times)
    average_time = total_time / len(times)
    variance = np.var(times, ddof=1)
    std_dev = np.std(times, ddof=1)
    percentiles = np.percentile(times, [10, 25, 50, 75, 90, 95, 99])
    return total_time, average_time, variance, std_dev, percentiles

def main(binary_file, n, output_file):
    times = run_benchmark(binary_file, n)
    total_time, average_time, variance, std_dev, percentiles = calculate_stats(times)
    output_str = f"Total time taken: {total_time:.6f} seconds\n"
    output_str += f"Average time taken: {average_time:.6f} seconds\n"
    output_str += f"Variance: {variance:.16f}\n"
    output_str += f"Standard deviation: {std_dev:.16f}\n"
    output_str += f"10th percentile: {percentiles[0]:.6f} seconds\n"
    output_str += f"25th percentile: {percentiles[1]:.6f} seconds\n"
    output_str += f"50th percentile: {percentiles[2]:.6f} seconds\n"
    output_str += f"75th percentile: {percentiles[3]:.6f} seconds\n"
    output_str += f"90th percentile: {percentiles[4]:.6f} seconds\n"
    output_str += f"95th percentile: {percentiles[5]:.6f} seconds\n"
    output_str += f"99th percentile: {percentiles[6]:.6f} seconds\n"
    with open(output_file, "w") as f:
        f.write(output_str)
    print("done")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run benchmark and calculate statistics')
    parser.add_argument('binary_file', type=str, help='Path to binary file')
    parser.add_argument('n', type=int, help='Number of times to run the binary')
    parser.add_argument('output_file', type=str, help='Path to output file')
    args = parser.parse_args()
    main(args.binary_file, args.n, args.output_file)
