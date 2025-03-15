# -*- coding: utf-8 -*-


import ctypes

user32 = ctypes.WinDLL("user32.dll")

# 현재 화면의 크기 가져오기
class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

rect = RECT()
user32.GetWindowRect(user32.GetDesktopWindow(), ctypes.byref(rect))

print("Screen Width: {rect.right - rect.left}")
print("Screen Height: {rect.bottom - rect.top}")

# MessageBox 표시
user32.MessageBoxW(None, u"안녕하세요! 점심시간을 이용해 공부 중입니다.", "Title", 0x40)
