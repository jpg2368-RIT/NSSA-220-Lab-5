#!/bin/python3.11

import subprocess

output=open('log.txt', 'w')
subprocess.call(['ls', '-la'], stdout=output)
