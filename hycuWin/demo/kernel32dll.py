# -*- coding: utf-8 -*-


import ctypes



# kernel32.dll 로드
kernel32 = ctypes.WinDLL("kernel32.dll")  # 또는 ctypes.CDLL("kernel32.dll")

# Windows 버전 확인 (GetVersion 함수 사용)
kernel32.GetVersion.restype = ctypes.c_ulong  # 반환 타입 설정
version = kernel32.GetVersion()

major = version & 0xFF
minor = (version >> 8) & 0xFF
build = (version >> 16) & 0xFFFF

print("Windows Version: {}.{}.{}".format(major, minor, build))
