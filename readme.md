# 해킹 보안 프로그래밍

## 시스템 프로그래밍 
-  Windows API(kernel32.dll) 
- = Mac [platform, os, psutil, subprocess]

---
- Windows는 kernel32.dll과 같은 WinAPI를 사용하여 정보를 가져옴
- Mac은 sysctl과 같은 Unix 명령어나 platform, psutil을 사용하여 정보를 가져옴
- Windows의 ctypes는 macOS에서 동작하지 않음, 대신 subprocess를 활용해야 함
- psutil은 Windows와 macOS 모두에서 사용 가능하여, 메모리 등의 정보 수집에 유용
  * macOS에서는 subprocess + sysctl을 주로 활용
  * Windows에서는 ctypes나 wmic를 사용