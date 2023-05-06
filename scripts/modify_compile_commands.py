import argparse
import json
import os
from pathlib import Path

def check_file_for_substring(file_path, substring):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    return substring in file_contents

def transform_compile_commands_file(input_file_path, output_file_path, opt_flag):
    with open(input_file_path, 'r') as f:
        compile_commands = json.load(f)

    transformed_commands = []
    for command in compile_commands:
        args = command['command'].split()

        output_file_name = args[args.index('-o')+1]

        clangpp_output = output_file_name.replace('.o', '.ll')

        clangpp_command = args[:args.index('-o')]
        clangpp_command.append(opt_flag)
        clangpp_command.append('-emit-llvm')
        clangpp_command.append('-o')
        clangpp_command.append(clangpp_output)
        clangpp_command.extend(args[args.index('-o')+2:])

        transformed_commands.append({
            'command': ' '.join(clangpp_command),
            'directory': command['directory'],
            'file': command['file']
        })

        opt_output = Path(command['directory']) / (clangpp_output + '.out')

        all_args = args.copy()
        all_args = all_args[1:-1]
        all_args = all_args[:all_args.index('-o')] + all_args[all_args.index('-o') + 2:]

        opt_command = ['python3.8']
        opt_command.append('optimizer.py')
        opt_command.append('--inliner_input_file={}'.format(Path(command['directory']) / clangpp_output))
        opt_command.append('--inliner_output_file={}'.format(opt_output))
        opt_command.append('--inliner_inline_lines_upper_bound={}'.format(500000000))
        opt_command.append('--inliner_cores_to_use={}'.format(16))
        opt_command.append('--inliner_arguments={}'.format(opt_flag))

        transformed_commands.append({
            'command': ' '.join(opt_command),
            'directory': os.path.dirname(os.path.abspath(__file__)),
            'file': command['file']
        })

        llc_output = Path(command['directory']) / (clangpp_output + '.s')

        llc_command = [args[0].replace('/clang++', '/llc')]
        llc_command.append('{}'.format(opt_output))
        llc_command.append(opt_flag)
        llc_command.append('-o')
        llc_command.append('{}'.format(llc_output))

        transformed_commands.append({
            'command': ' '.join(llc_command),
            'directory': os.path.dirname(os.path.abspath(__file__)),
            'file': command['file']
        })

        final_command = ['as', str(llc_output), '-o', output_file_name]

        transformed_commands.append({
            'command': ' '.join(final_command),
            'directory': command['directory'],
            'file': command['file']
        })


    with open(output_file_path, 'w') as f:
        json.dump(transformed_commands, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build with optimizer')

    parser.add_argument('--build_input', type=str, required=True, help='изначальный compile_commands.json')
    parser.add_argument('--build_output', type=str, required=True, help='файл модифицированного compile_commands.json')
    parser.add_argument('--build_opt_flag', type=str, default="", help='O?')

    script_args = parser.parse_args()

    transform_compile_commands_file(script_args.build_input, script_args.build_output, script_args.build_opt_flag)
