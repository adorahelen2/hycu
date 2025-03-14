
# -*- coding: utf-8 -*-

import ctypes

# ExitWindowsEx 함수 사용 (Windows 종료)
user32 = ctypes.WinDLL("user32.dll")

EWX_SHUTDOWN = 0x00000001  # 시스템 종료 플래그
token = ctypes.c_void_p()  # 관리자 권한 필요

result = user32.ExitWindowsEx(EWX_SHUTDOWN, 0)
if result:
    print("System shutting down...")
else:
    print("Shutdown failed.")
