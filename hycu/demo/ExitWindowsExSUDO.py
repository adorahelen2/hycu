# -*- coding: utf-8 -*-


import ctypes
import ctypes.wintypes

# Define LUID structure
class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", ctypes.wintypes.DWORD),
        ("HighPart", ctypes.wintypes.LONG),
    ]

# AdjustTokenPrivileges 사용 (권한 조정)
def adjust_privilege(priv):
    flags = (ctypes.c_int * 3)()
    ctypes.windll.advapi32.OpenProcessToken(ctypes.windll.kernel32.GetCurrentProcess(), 0x0020 | 0x0008, flags)
    token = flags[0]

    luid = LUID()
    ctypes.windll.advapi32.LookupPrivilegeValueW(None, priv, ctypes.byref(luid))

    class TOKEN_PRIVILEGES(ctypes.Structure):
        _fields_ = [("PrivilegeCount", ctypes.wintypes.DWORD),
                    ("Luid", LUID),
                    ("Attributes", ctypes.wintypes.DWORD)]

    privileges = TOKEN_PRIVILEGES(1, luid, 0x00000002)  # SE_PRIVILEGE_ENABLED
    ctypes.windll.advapi32.AdjustTokenPrivileges(token, False, ctypes.byref(privileges), 0, None, None)

# 권한 조정
adjust_privilege('SeShutdownPrivilege')

# ExitWindowsEx 함수 사용 (Windows 종료)
user32 = ctypes.WinDLL("user32.dll")

EWX_SHUTDOWN = 0x00000001  # 시스템 종료 플래그

result = user32.ExitWindowsEx(EWX_SHUTDOWN, 0)
if result:
    print("System shutting down...")
else:
    print("Shutdown failed.")



# 코드가 실패하는 이유는 LUID 구조체가 ctypes.wintypes 모듈에 직접적으로 포함되어 있지 않기 때문입니다. 이를 해결하기 위해 LUID 구조체를 수동으로 정의해야 합니다. 그리고 또 하나, 권한 조정을 위한 코드가 제대로 실행되지 않을 경우 시스템 종료 권한이 없어서 실패할 수도 있습니다.
#
# 위의 예제 코드에서 LUID 구조체를 수동으로 정의하고 권한을 조정하는 방법을 다시 확인해보세요. 중요한 점은 다음과 같습니다:
#
# LUID 구조체를 수동으로 정의
#
# 권한 조정을 위해 SeShutdownPrivilege를 활성화