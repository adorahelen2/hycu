# -*- coding: utf-8 -*-

import ctypes

# SYSTEM_INFO 구조체 정의
class SYSTEM_INFO(ctypes.Structure):
    _fields_ = [
        ("wProcessorArchitecture", ctypes.c_ushort),
        ("wReserved", ctypes.c_ushort),
        ("dwPageSize", ctypes.c_uint),
        ("lpMinimumApplicationAddress", ctypes.c_void_p),
        ("lpMaximumApplicationAddress", ctypes.c_void_p),
        ("dwActiveProcessorMask", ctypes.c_ulong),
        ("dwNumberOfProcessors", ctypes.c_uint),
        ("dwProcessorType", ctypes.c_uint),
        ("dwAllocationGranularity", ctypes.c_uint),
        ("wProcessorLevel", ctypes.c_ushort),
        ("wProcessorRevision", ctypes.c_ushort),
    ]

# kernel32.dll 로드
kernel32 = ctypes.WinDLL("kernel32.dll")

# SYSTEM_INFO 구조체 생성 및 초기화
sys_info = SYSTEM_INFO()
kernel32.GetSystemInfo(ctypes.byref(sys_info))

print("CPU Architecture:", sys_info.wProcessorArchitecture)
print("Number of Processors:", sys_info.dwNumberOfProcessors)
print("Page Size:", sys_info.dwPageSize)
