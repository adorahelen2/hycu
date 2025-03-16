
---

# DLL 로딩 및 함수 호출 방식 (ctypes 활용)

Python에서 Windows의 **DLL(Dynamic Link Library)**을 로드하고 사용하는 방법을 자세히 설명하겠습니다. `ctypes` 모듈을 사용하면 Python 코드에서 C 라이브러리를 직접 호출할 수 있습니다.

---

## 1. DLL 로딩 방법

Python에서는 `ctypes`를 사용해 여러 방식으로 DLL을 로드할 수 있습니다.

### ✅ ctypes에서 제공하는 DLL 로딩 클래스

`ctypes`에는 네 가지 주요 DLL 클래스가 있습니다. 각 클래스는 특정 유형의 DLL을 로드하는 데 사용됩니다.

| 클래스  | 설명                                        |
|---------|-------------------------------------------|
| `CDLL`  | 표준 C 호출 규약을 사용하는 DLL을 로드함. 일반적인 경우 사용 |
| `WinDLL`| Windows의 `stdcall` 호출 규약을 사용하는 DLL을 로드 |
| `OleDLL`| OLE(객체 연결 및 포함) 관련 DLL을 로드. `stdcall` 사용 |
| `PyDLL` | Python에서 사용할 수 있도록 설계된 DLL을 로드 |

#### 예제: kernel32.dll을 로드하는 방법

```python
import ctypes

# CDLL 사용 (기본 C 호출 규약)
c_dll = ctypes.CDLL("kernel32.dll")

# WinDLL 사용 (Windows 전용, stdcall 호출 규약)
w_dll = ctypes.WinDLL("kernel32.dll")
```

### ✅ ctypes.LibraryLoader 객체 활용

`ctypes`의 `LibraryLoader` 객체를 사용하면 `CDLL`, `WinDLL` 등을 쉽게 불러올 수 있습니다.

```python
from ctypes import windll, cdll

kernel32 = windll.kernel32  # Windows API 로드
msvcrt = cdll.msvcrt        # 표준 C 라이브러리 로드
```

---

## 2. DLL 함수 호출 방법

DLL을 로드한 후, 내부 함수를 호출할 수 있습니다.

### ✅ DLL 함수에 직접 접근

#### 방법 1: DLL 객체의 속성으로 접근

```python
GetTickCount = kernel32.GetTickCount
print(GetTickCount())  # 시스템 부팅 이후 경과한 시간(ms)
```

#### 방법 2: `getattr()`을 사용하여 접근

```python
import ctypes

get_version = getattr(ctypes.windll.kernel32, "GetVersion")
print(get_version())  # Windows 버전 정보 가져오기
```

#### 방법 3: DLL 객체 인덱스를 통한 접근

```python
print(kernel32[0])  # 첫 번째 함수 (주소 반환)
```

---

## 3. DLL 함수 호출과 데이터 변환

Python과 C는 서로 다른 데이터 타입을 사용하므로, `ctypes`를 이용해 변환해야 합니다.

### ✅ DLL 함수의 리턴 타입 설정

DLL에서 반환되는 값의 타입을 `restype` 속성을 사용해 설정할 수 있습니다.

```python
kernel32.GetTickCount.restype = ctypes.c_ulong
result = kernel32.GetTickCount()
print(result)  # GetTickCount()의 반환값을 올바르게 해석
```

### ✅ DLL 함수의 인자 타입 설정

함수의 매개변수 타입을 `argtypes` 속성으로 지정해야 정확한 데이터 변환이 가능합니다.

```python
kernel32.Sleep.argtypes = [ctypes.c_uint]  # Sleep() 함수는 unsigned int를 인자로 받음
kernel32.Sleep(1000)  # 1초 동안 대기
```

---

## 4. ctypes의 데이터 변환 (Wrapper 타입)

Python의 기본 데이터 타입을 C의 타입으로 변환하는 `ctypes`의 데이터 타입을 정리하면 다음과 같습니다.

| ctypes 데이터 타입 | C 데이터 타입           | 설명                        |
|--------------------|--------------------------|-----------------------------|
| `c_char`           | `char`                  | 1바이트 문자                 |
| `c_wchar`          | `wchar_t`              | 와이드 문자 (유니코드)        |
| `c_byte`           | `signed char`          | 1바이트 정수 (부호 있음)      |
| `c_ubyte`          | `unsigned char`        | 1바이트 정수 (부호 없음)      |
| `c_short`          | `short`                | 2바이트 정수                 |
| `c_ushort`         | `unsigned short`       | 2바이트 정수 (부호 없음)      |
| `c_int`            | `int`                  | 4바이트 정수                 |
| `c_uint`           | `unsigned int`         | 4바이트 정수 (부호 없음)      |
| `c_long`           | `long`                 | 시스템 기본 정수 크기 (일반적으로 4바이트) |
| `c_ulong`          | `unsigned long`        | 4바이트 정수 (부호 없음)      |
| `c_longlong`       | `long long`            | 8바이트 정수                 |
| `c_ulonglong`      | `unsigned long long`   | 8바이트 정수 (부호 없음)      |
| `c_float`          | `float`                | 4바이트 부동소수점           |
| `c_double`         | `double`               | 8바이트 부동소수점           |
| `c_char_p`         | `char *`               | C 문자열 (바이트)            |
| `c_wchar_p`        | `wchar_t *`            | 유니코드 문자열              |
| `c_void_p`         | `void *`               | 포인터                      |

---

## 5. 콜백 함수 (Callback Function)

DLL이 Python에서 정의한 함수를 호출하려면 콜백 함수를 정의해야 합니다.

### ✅ 콜백 함수란?
- DLL에서 실행될 때 Python에서 정의한 특정 함수를 호출하도록 설정하는 함수.
- C에서 함수를 포인터로 전달하는 것과 비슷한 방식.

### ✅ 콜백 함수 구현 절차
1. 콜백 함수가 호출될 DLL 함수 확인  
2. 콜백 함수의 유형 지정  
3. 콜백 함수 정의  
4. 콜백 객체 생성  
5. DLL 함수 호출 시 콜백 전달  

### ✅ 콜백 함수 예제

```python
import ctypes

# 콜백 함수의 반환 타입과 인자 타입을 정의 (예: int 함수(int, int))
CALLBACK_FUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)

# 콜백 함수 정의
def my_callback(a, b):
    print(f"Callback 함수 호출됨: {a} + {b}")
    return a + b

# 콜백 객체 생성
callback_func = CALLBACK_FUNC(my_callback)

# DLL 함수가 이 콜백을 호출하도록 설정
# (예제에서는 DLL이 없으므로 직접 호출)
result = callback_func(10, 20)
print("결과:", result)
```

### ✅ 실제 DLL과 연동하는 콜백 함수

Windows API의 `EnumWindows()` 함수는 실행 중인 모든 창을 나열하며, 콜백 함수로 창 정보를 받을 수 있습니다.

```python
import ctypes

# EnumWindows 콜백 함수 정의
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

def enum_windows_callback(hwnd, lParam):
    print(f"창 핸들: {hwnd}")
    return True  # 계속해서 다음 창을 검색

# 콜백 객체 생성
callback = WNDENUMPROC(enum_windows_callback)

# EnumWindows 호출 (User32.dll 사용)
user32 = ctypes.windll.user32
user32.EnumWindows(callback, 0)
```

---

## 6. 정리

- **DLL을 로드하는 방법**  
  `CDLL`, `WinDLL`, `OleDLL`, `PyDLL`을 이용해 DLL을 불러옴.  
  `windll`, `cdll`을 활용하여 쉽게 접근 가능.

- **DLL 함수 호출**  
  `restype`으로 반환 타입 설정  
  `argtypes`으로 매개변수 타입 지정  
  `getattr()`, 속성 접근, 인덱스를 활용하여 함수 호출 가능

- **데이터 변환**  
  `ctypes`의 `c_int`, `c_char_p` 등 C 타입을 활용하여 Python과 C 간 변환 가능

- **콜백 함수**  
  Python에서 정의한 함수를 C 함수처럼 DLL이 호출할 수 있도록 설정  
  `CFUNCTYPE`, `WINFUNCTYPE`을 사용해 콜백 유형 지정

💡 **ctypes**를 활용하면 Python에서도 Windows API를 쉽게 제어할 수 있으며, 보안 및 해킹 연구에도 활용 가능합니다! 🚀

--- 

