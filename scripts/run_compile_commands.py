import argparse
import json
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description='Execute commands from a compile_commands.json file')
    parser.add_argument('--compile_command_path', type=str, required=True, help='path to the compile_commands.json file')
    args = parser.parse_args()

    with open(args.compile_command_path) as f:
        commands = json.load(f)

    for command in commands:
        os.chdir(command['directory'])
        print(f"Running {command['command']}")
        subprocess.run(command['command'].split())

if __name__ == '__main__':
    main()
