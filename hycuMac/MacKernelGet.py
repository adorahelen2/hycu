# -*- coding: utf-8 -*-
import platform
import os
import subprocess
import psutil

# OS 정보 가져오기
os_name = platform.system()
os_version = platform.mac_ver()[0]

# 메모리 정보 가져오기
memory_info = psutil.virtual_memory()
total_memory = memory_info.total  # 총 메모리 (바이트)
available_memory = memory_info.available  # 사용 가능한 메모리 (바이트)

# CPU 정보 가져오기
cpu_info = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True).decode().strip()

# 하드웨어 정보 가져오기
hardware_model = subprocess.check_output("sysctl -n hw.model", shell=True).decode().strip()

print(f"OS: {os_name} {os_version}")
print(f"CPU: {cpu_info}")
print(f"Hardware Model: {hardware_model}")
print(f"Total Memory: {total_memory / (1024**3):.2f} GB")
print(f"Available Memory: {available_memory / (1024**3):.2f} GB")