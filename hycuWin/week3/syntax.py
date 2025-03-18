# -*- coding: utf-8 -*-

import os
from ctypes import *

# 1. C 구조체 & 유니온 정의
class MyStruct(Structure):
    _fields_ = [("integer", c_int), ("float_num", c_float), ("char", c_char)]

class MyUnion(Union):
    _fields_ = [("integer", c_int), ("float_num", c_float)]

# 구조체 & 유니온 사용
struct_instance = MyStruct(10, 3.14, "A")
print "Struct - Integer:", struct_instance.integer, ", Float:", struct_instance.float_num, ", Char:", struct_instance.char

union_instance = MyUnion()
union_instance.integer = 42
print "Union - Integer:", union_instance.integer, ", Float:", union_instance.float_num  # 같은 메모리 사용

# 2. ctypes 배열
IntArray = c_int * 5
arr = IntArray(1, 2, 3, 4, 5)
print "Array Elements:", [arr[i] for i in range(5)]

# 3. 포인터 활용
val = c_int(100)
ptr = pointer(val)
print "Pointer Value:", ptr.contents.value

# 4. 가변형 메모리 블록
buffer = create_string_buffer("Hello, ctypes!", 20)
print "Buffer:", buffer.value

# 5. C 라이브러리 함수 사용 (Linux/macOS: libc.so.6, Windows: msvcrt.dll)
libc = cdll.msvcrt if os.name == "nt" else CDLL("libc.so.6")
libc.puts.argtypes = [c_char_p]
libc.puts.restype = c_int
libc.puts("Hello from C function!")

# 6. 직접 만든 C 함수 호출 (myfunc.so / Windows는 DLL)
mylib = CDLL(r"C:\Users\kmkim\PycharmProjects\hycu\hycuWin\week3\myfunc.dll")
##  DLL 파일이 프로젝트 폴더에 없는 경우
##  ❌ Windows에서 .dll 파일이 없는 경우 에러 발생
##  ✅ 해결 방법: myfunc.dll을 빌드하여 프로젝트 폴더에 추가


# C 함수 바인딩
mylib.add.argtypes = [c_int, c_int]
mylib.add.restype = c_int

result = mylib.add(5, 10)
print "C Function - 5 + 10 =", result

# 포인터를 이용한 C 함수 호출
mylib.modify_value.argtypes = [POINTER(c_int)]
mylib.modify_value.restype = None

val = c_int(20)
mylib.modify_value(byref(val))
print "C Function - Modified value:", val.value

# 7. CFUNCTYPE을 사용한 Python 함수를 C 스타일 콜백으로 변환
CALLBACK_FUNC = CFUNCTYPE(c_int, c_int, c_int)

def py_add(a, b):
    return a + b

c_func = CALLBACK_FUNC(py_add)
print "Python Callback in C Style:", c_func(3, 7)

# 8. Windows API 호출 (Windows 환경에서만 실행 가능)
if os.name == "nt":
    user32 = windll.user32
    prototype = WINFUNCTYPE(c_int, c_void_p, c_wchar_p, c_wchar_p, c_uint)
    paramflags = ((1, "hWnd"), (1, "lpText"), (1, "lpCaption"), (1, "uType"))
    MessageBox = prototype(("MessageBoxW", user32), paramflags)
    MessageBox(None, u"CTypes를 사용한 Windows API 호출!", u"알림", 0)
