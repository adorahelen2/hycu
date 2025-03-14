# -*- coding: utf-8 -*-

import ctypes

kernel32 = ctypes.WinDLL("kernel32.dll")

# VirtualAlloc (메모리 할당)
ptr = kernel32.VirtualAlloc(
    None,  # 시스템이 자동으로 주소 결정
    4096,  # 4KB 할당
    0x1000,  # MEM_COMMIT
    0x04,  # PAGE_READWRITE
)

if ptr:
    print("Memory allocated at:", hex(ptr))
else:
    print("Memory allocation failed!")


# VirtualFree (메모리 해제)
if ptr:
    kernel32.VirtualFree(ptr, 0, 0x8000)  # MEM_RELEASE
    print("Memory freed.")
