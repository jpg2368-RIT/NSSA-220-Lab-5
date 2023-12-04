#!/bin/python3.11

import subprocess

f = open('test.txt', 'w')

process = subprocess.run(['ls','-la'], stdout=subprocess.PIPE)

f.write(str(process.stdout))

f.close()

