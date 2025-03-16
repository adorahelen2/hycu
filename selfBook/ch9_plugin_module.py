# Author : adorahelen
import os
import hashlib


class KavMain:

    def __init__(self):
        """ 플러그인 엔진 초기화 """
        self.vdb = []  # 악성코드 데이터베이스
        self.init()

# init 함수는 백신 커널이 플러그인 엔진에게 악성코드 진단/치료를 위해 초기화 작업을 하기 위해 호출한다면,
    def init(self):
        """ 플러그인 엔진을 초기화하고, 악성코드 데이터베이스를 로드 """
        print("[*] Plugin Engine Initialized")
        self.vdb = {
            "44d88612fea8": "ERICA TEST",
            "77bff0b14402": "Ransomware",
            "888999222rjr": "Trojan"
        }

# uninit 함수는 백신 커널이 플러그인 엔진에게 이제 잠시 뒤 백신 엔진 전체가 종료될 것을 알려주는 시점에 호출 된다.
    ## 따라서, init 함수에서 선언된 패턴 로딩 & 메모리 할당 등의 작업이 있다면, 메모리 해제 등이 필요하다.
    def uninit(self):
        """ 플러그인 엔진 종료 """
        print("[*] Plugin Engine Uninitialized")
        self.vdb = {}

# 악성코드를 검사하는 부분이 실제 소스코드의 상당 부분을 차지한다. 따라서 scan 함수가 플러그인 엔진에서 가장 핵심이다.
    def scan(self, file_path):
        """ 주어진 파일의 해시값을 검사하여 악성코드 여부 판단 """
        if not os.path.exists(file_path):
            return False, "Error: File Not Found"

        with open(file_path, "rb") as fp:
            buf = fp.read()

        file_hash = hashlib.md5(buf).hexdigest()
        if file_hash in self.vdb:
            return True, self.vdb[file_hash]  # 악성코드 발견 시 (True, 악성코드 이름) 반환
        return False, "Clean"  # 악성코드 미발견 시 (False, "Clean") 반환

    def disinfect(self, file_path):
        """ 감염된 파일 삭제 """
        infected, vname = self.scan(file_path)
        if infected:
            os.remove(file_path)
            return f"[+] {file_path} ({vname}) removed successfully!"
        return f"[+] {file_path} is clean."

    def listvirus(self):
        """ 플러그인이 진단 및 치료 가능한 악성코드 목록 반환 """
        return list(self.vdb.values())

    def getinfo(self):
        """ 플러그인 엔진의 기본 정보 제공 """
        return {
            "name": "KavPluginEngine",
            "version": "1.0",
            "author": "Security Engineer",
            "description": "Simple Antivirus Plugin Engine"
        }


# 테스트 코드 실행
if __name__ == "__main__":
    kav = KavMain()

    test_file = "test_malware.exe"

    print("\n[*] Scan Result:", kav.scan(test_file))
    print("\n[*] Disinfection Result:", kav.disinfect(test_file))
    print("\n[*] Virus List:", kav.listvirus())
    print("\n[*] Engine Info:", kav.getinfo())

    kav.uninit()

    # 여기서 끝이 아니라, 백신 엔진이 악성코드 유포자의 손에 넘어가, 분석되고 악용될 가능성을 고려한다.
    # => 암호화&복호화 적용하여, 소스코드가 넘어가도 파악할 수 없도록 (ch6, ch10)
