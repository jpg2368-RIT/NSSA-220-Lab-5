#!/bin/python3.11

import subprocess

result = subprocess.run(['echo', 'Hello from bash!'], capture_output=True, text=True)
output_from_bash = result.stdout.strip()

print(f"Captured: {output_from_bash}")

