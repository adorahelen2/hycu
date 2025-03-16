# 해킹 보안 프로그래밍

## **1. 시스템 프로그래밍**
-  Windows API(kernel32.dll) 
- = Mac [platform, os, psutil, subprocess]

---
- Windows는 kernel32.dll과 같은 WinAPI를 사용하여 정보를 가져옴
- Mac은 sysctl과 같은 Unix 명령어나 platform, psutil을 사용하여 정보를 가져옴
- Windows의 ctypes는 macOS에서 동작하지 않음, 대신 subprocess를 활용해야 함
- psutil은 Windows와 macOS 모두에서 사용 가능하여, 메모리 등의 정보 수집에 유용
  * macOS에서는 subprocess + sysctl을 주로 활용
  * Windows에서는 ctypes나 wmic를 사용

## **2. UNIX 계열 vs. Windows 계열**

### **🟢 UNIX 계열 (Unix-like)**
| UNIX 계열         | 설명                                                      |
|--------------------|----------------------------------------------------------|
| **BSD**           | UNIX에서 파생된 오픈소스 OS, macOS의 기반.                |
| **Linux**         | 1991년 **리누스 토르발스(Linus Torvalds)**가 개발한 커널. |
| **macOS**         | BSD 기반이며, Darwin이라는 커널 사용.                     |
| **AIX, Solaris**  | 기업용 UNIX 시스템.                                       |

💡 UNIX 계열은 **POSIX(Portable Operating System Interface)** 표준을 따름

---

### **🔵 Windows 계열**
| Windows 계열                     | 설명                                                               |
|-----------------------------------|-------------------------------------------------------------------|
| **MS-DOS**                       | 1981년, 마이크로소프트가 IBM PC용으로 개발한 OS.                   |
| **Windows 1.0 ~ ME (9x 커널)**   | MS-DOS 기반 GUI OS.                                                |
| **Windows NT 계열 (2000~현재)**  | MS-DOS에서 완전히 독립된 구조 (UNIX와 무관).                      |

💡 Windows는 MS-DOS에서 발전한 OS로, UNIX 계열과 구조가 다릅니다.  
최근 Windows 10, 11에서는 **WSL(Windows Subsystem for Linux)**를 통해 UNIX 명령어를 사용 가능
---



## **3. Windows vs. UNIX 계열의 차이점**
### (보안 및 해킹, 바이러스 분석 관점)

---

| **특징**             | **UNIX 계열 (Linux/macOS)**                         | **Windows**                                   |
|----------------------|----------------------------------------------------|-----------------------------------------------|
| **커널 구조**        | 모놀리식 또는 마이크로커널 (보안 강화 가능, 커널 패치 용이) | 하이브리드 (NT 커널, 높은 호환성 but 공격 표면 증가) |
| **기반 아키텍처**     | POSIX 준수, 다중 사용자 구조 (기본적으로 루트 권한 제한)   | NT 아키텍처, 사용자 중심 설계 (관리자 권한 요청 많음) |
| **파일 시스템**      | ext4, ZFS, APFS (저널링 지원, 파일권한 세분화)         | NTFS, FAT32 (NTFS ACL 기반 접근 제어)          |
| **명령어 인터페이스** | 터미널(Bash, Zsh, Fish), 강력한 스크립팅 지원          | PowerShell, CMD (PowerShell은 강력한 자동화 기능) |
| **오픈소스 여부**    | 대부분 오픈소스 (소스코드 분석 가능, 취약점 연구 쉬움)    | 폐쇄형 시스템 (코드 접근 어려움, 리버스 엔지니어링 필요) |
| **바이러스 확산 가능성**| 제한적 (엄격한 권한 제어, SELinux/AppArmor 등 보안 모듈) | 높음 (대중성 + 실행 파일 중심 구조, DLL 인젝션 가능) |
| **악성코드 제작 난이도**| 높음 (사용자 권한 제한, 다양한 보안 모듈 존재)          | 상대적으로 낮음 (Windows API 활용 용이)         |
| **포렌식 및 분석 도구**| strace, lsof, auditd, Ghidra, Volatility 활용 가능    | Process Explorer, WinDbg, Sysinternals, Volatility |
| **백도어·루트킷**    | LKM (Loadable Kernel Module) 기반 루트킷 제작 가능     | 커널 드라이버 기반 루트킷, DLL 인젝션, UAC 우회 가능 |
| **취약점 유형**      | Buffer Overflow, Race Condition, SUID 바이너리 취약점 | DLL Hijacking, Token Impersonation, UAC Bypass |

---

## **🔍 보안 프로그래밍 & 해킹 연구 관점에서의 주요 차이점**

1. **Windows는 바이러스 타겟이 많다.**
   - 시장 점유율이 높고, 실행 파일(.exe, .dll)의 특성 때문에 악성코드 제작이 용이.
   - **DLL 인젝션**, 프로세스 가로채기 등이 활발히 연구되고 사용됨.

2. **Linux는 기본적으로 보안성이 높다.**
   - 루트 권한이 기본적으로 제한됨.  
     예: `chmod`, `chown`, `sudo` 명령을 통해 접근 제어.
   - **SELinux**, **AppArmor** 같은 커널 수준의 보안 모듈 제공.
   - 단, **LKM 루트킷**이나 취약한 SUID 바이너리를 통한 **권한 상승 공격**은 여전히 가능.

3. **macOS는 보안이 강하지만 바이패스 가능성 존재.**
   - BSD 기반이라 강력한 보안 정책 제공(Gatekeeper, SIP 등).
   - 그러나 취약한 서명된 실행 파일을 악용한 공격(XProtect 우회)이 가능.
   - Objective-C 기반의 Mach-O 바이너리 분석 기술 요구됨.

4. **Windows는 리버스 엔지니어링이 활발히 연구됨.**
   - **IDA Pro, x64dbg, WinDbg** 등의 도구가 강력.
   - **API Hooking**, **Process Injection** 등의 공격 기법이 일반적.

5. **Linux는 서버 공격, Windows는 사용자 공격이 많음.**
   - **Linux**:
     - 주로 웹 서버, SSH, 컨테이너(Docker)의 취약점을 공격 목표로 설정.
   - **Windows**:
     - 피싱, 매크로 악성코드, 랜섬웨어를 통한 사용자 공격이 많음.

---


