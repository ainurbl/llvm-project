import sys
import time
import subprocess
import numpy as np
import argparse
import os

def makeInput(path, opt, o):
    input = './' + path + '/' + path
    if o != '':
        input += '_' + o
    if opt != '':
        input += '_' + opt
    return input

def makeOutput(path, opt, o, runs):
    output = './results/' + path + "/{}/".format(runs)
    if not os.path.exists(output):
        os.makedirs(output)
    if o != '':
        output += o
    if opt != '':
        output += '.' + opt
    return "{}.txt".format(output)

def main():
    os=['O0', 'O2', 'O3']
    opts=['BASE', 'OPT']
    paths=['XML']
    runs=[5, 10, 2000, 5000]
    for run in runs:
        for o in os:
            for path in paths:
                for opt in opts:
                    subprocess.run(['taskset', '-c', '1', 'python3', 'pbench.py', makeInput(path, opt, o), '{}'.format(run), makeOutput(path, opt, o, run)])

if __name__ == '__main__':
    
    main()
