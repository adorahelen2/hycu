class VaccineKernel:
    def __init__(self):
        self.plugins = []  # 로드된 플러그인 목록

    def load_plugins(self, plugin_list):
        """플러그인 엔진을 로드 및 초기화"""
        for plugin in plugin_list:
            plugin.init()
            self.plugins.append(plugin)

    def unload_plugins(self):
        """모든 플러그인 엔진을 종료"""
        for plugin in self.plugins:
            plugin.uninit()
        self.plugins.clear()

    def scan_file(self, filepath):
        """파일을 검사하여 감염 여부 확인"""
        for plugin in self.plugins:
            result = plugin.scan(filepath)
            if result:
                print(f"[!] 감염 파일 발견: {filepath} - {result}")
                return result
        print(f"[*] 파일 안전: {filepath}")
        return None

    def disinfect_file(self, filepath):
        """감염된 파일을 치료"""
        for plugin in self.plugins:
            if plugin.disinfect(filepath):
                print(f"[+] 치료 완료: {filepath}")
                return True
        print(f"[-] 치료 실패: {filepath}")
        return False

    def get_virus_list(self):
        """모든 플러그인의 진단 가능한 악성코드 목록 반환"""
        virus_list = []
        for plugin in self.plugins:
            virus_list.extend(plugin.listvirus())
        return virus_list

    def get_plugin_info(self):
        """로드된 플러그인의 정보를 반환"""
        for plugin in self.plugins:
            print(plugin.getinfo())


# 테스트용 플러그인 클래스 예시
class ExamplePlugin:
    def init(self):
        print("Example Plugin 초기화됨")

    def uninit(self):
        print("Example Plugin 종료됨")

    def scan(self, filepath):
        return "TestVirus" if "infected" in filepath else None

    def disinfect(self, filepath):
        return "infected" in filepath

    def listvirus(self):
        return ["TestVirus"]

    def getinfo(self):
        return "Example Plugin v1.0"


# 백신 커널 실행 예제
if __name__ == "__main__":
    kernel = VaccineKernel()
    test_plugin = ExamplePlugin()

    kernel.load_plugins([test_plugin])
    kernel.scan_file("safe_file.txt")
    kernel.scan_file("infected_file.exe")
    kernel.disinfect_file("infected_file.exe")
    kernel.get_plugin_info()
    kernel.unload_plugins()

    # 백신 콘솔 프로그램 개발은 간단함
    # GUI 의 경우, 별도의 책으로 다룰 만큼 분량이 많음