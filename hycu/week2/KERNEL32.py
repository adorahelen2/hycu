# -*- coding: utf-8 -*-

import ctypes

# Load kernel32.dll
kernel32 = ctypes.WinDLL("kernel32.dll")

# Define SYSTEMTIME structure
class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ("wYear", ctypes.c_ushort),
        ("wMonth", ctypes.c_ushort),
        ("wDayOfWeek", ctypes.c_ushort),
        ("wDay", ctypes.c_ushort),
        ("wHour", ctypes.c_ushort),
        ("wMinute", ctypes.c_ushort),
        ("wSecond", ctypes.c_ushort),
        ("wMilliseconds", ctypes.c_ushort)
    ]

# Get system uptime
uptime = kernel32.GetTickCount()  # 시스템이 부팅된 이후 경과된 시간(밀리초)
print("System Uptime (ms):", uptime)

# Get system time
sys_time = SYSTEMTIME()
kernel32.GetSystemTime(ctypes.byref(sys_time))

print("Current System Time: {}/{}/{} {}:{}:{}.{}".format(
    sys_time.wYear,
    sys_time.wMonth,
    sys_time.wDay,
    sys_time.wHour,
    sys_time.wMinute,
    sys_time.wSecond,
    sys_time.wMilliseconds
))
