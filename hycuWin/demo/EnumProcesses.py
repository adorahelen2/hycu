# -*- coding: utf-8 -*-


import ctypes
import ctypes.wintypes

psapi = ctypes.WinDLL("Psapi.dll")
kernel32 = ctypes.WinDLL("kernel32.dll")


# 프로세스 ID 목록 가져오기
def get_process_list():
    arr = (ctypes.wintypes.DWORD * 1024)()
    size_needed = ctypes.wintypes.DWORD()

    if psapi.EnumProcesses(ctypes.byref(arr), ctypes.sizeof(arr), ctypes.byref(size_needed)):
        num_procs = size_needed.value // ctypes.sizeof(ctypes.wintypes.DWORD)
        return arr[:num_procs]
    return []


process_ids = get_process_list()
print("Running Processes:", process_ids[:100])  # 처음 10개 프로세스 출력
