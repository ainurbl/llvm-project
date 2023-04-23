import argparse
import subprocess
import os
import shutil
from scipy.optimize import differential_evolution
from pathlib import Path


parser = argparse.ArgumentParser(description='Optimizer script')

parser.add_argument('--inliner_input_ll_file', type=str, required=True, help='название файла с LLVM IR кодом, который нужно оптимизировать')
parser.add_argument('--inliner_output_ll_file', type=str, required=True, help='название файла, в который надо положить оптимизированный LLVM IR')

parser.add_argument('--inliner_inline_lines_upper_bound', type=int, required=True, help='верхняя граница добавочного кода за счет агрессивного инлайна')

parser.add_argument('--inliner_opt_path', type=str, default='/home/intersection/Documents/MCS/Diploma/llvm-project/build/bin/opt', help='путь к opt')
parser.add_argument('--inliner_arguments', type=str, default='', help='аргументы для opt в формате \"-O2 -fms-hotpatch\"')

parser.add_argument('--inliner_cost_left_bound', type=int, default=0, help='левая граница перебора inliner_cost')
parser.add_argument('--inliner_cost_right_bound', type=int, default=100, help='правая граница перебора inliner_cost')
parser.add_argument('--inliner_threshold_left_bound', type=int, default=0, help='левая граница перебора inliner_threshold')
parser.add_argument('--inliner_threshold_right_bound', type=int, default=500, help='правая граница перебора inliner_threshold')
parser.add_argument('--inliner_tmp_folder_name', type=str, default='.optimizer', help='название подпапки в текущей директории, в которую складывается служебная информация')


script_args = parser.parse_args()


bounds = [(script_args.inliner_cost_left_bound, script_args.inliner_cost_right_bound),
           (script_args.inliner_threshold_left_bound, script_args.inliner_threshold_right_bound)] 

def get_file_length(file_path):
    with open(file_path, "r") as f:
        contents = f.read()
        length = len(contents)
        return length

def optimize(args):
    inliner_cost = int(args[0])
    inliner_threshold = int(args[1])
    cmd = "{} -S {} -my-inliner -my-inliner-cost={} -my-inliner-threshold={} {} -o {}/robin_hood.opt2.{}.{}.ll".format(script_args.inliner_opt_path, script_args.inliner_arguments, inliner_cost, inliner_threshold, script_args.inliner_input_ll_file, script_args.inliner_tmp_folder_name, inliner_cost, inliner_threshold)
    subprocess.check_output(cmd, shell=True)
    file_length = get_file_length("{}/robin_hood.opt2.{}.{}.ll".format(script_args.inliner_tmp_folder_name, inliner_cost, inliner_threshold))
    if file_length - baseline_length > script_args.inliner_inline_lines_upper_bound:
        return 0
    return -file_length
    
def create_tmp_folder(): 
    path = Path(script_args.inliner_tmp_folder_name)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)

def clean_tmp_folder(file_name):
    for _, _, files in os.walk(script_args.inliner_tmp_folder_name):
        for name in files:
            if name != file_name:
                os.remove(Path(script_args.inliner_tmp_folder_name) / name)
            else:
                shutil.copy(Path(script_args.inliner_tmp_folder_name) / name, script_args.inliner_output_ll_file)

def opt_default():
    cmd = "{} -S {} {} -o {}/robin_hood.opt1.ll".format(script_args.inliner_opt_path, script_args.inliner_arguments, script_args.inliner_input_ll_file, script_args.inliner_tmp_folder_name)
    subprocess.check_output(cmd, shell=True)


create_tmp_folder()
opt_default()
baseline_length = get_file_length("{}/robin_hood.opt1.ll".format(script_args.inliner_tmp_folder_name))
print("Baseline length: {}".format(baseline_length))

result = differential_evolution(optimize, bounds, tol=100)
best_inliner_cost, best_inliner_threshold = result.x.astype(int)
best_file_name = "robin_hood.opt2.{}.{}.ll".format(best_inliner_cost, best_inliner_threshold)

print("Maximum length: {}".format(-result.fun))

clean_tmp_folder(best_file_name)
