#!/bin/python3.11

import subprocess

with open('output.txt','w') as file:
    procvar = subprocess.run(['ls', '-la', 'dne'], stderr=subprocess.DEVNULL)

file.close()

