# Author : adorahelen
import sys  # 시스템 관련 기능을 사용하기 위한 모듈
from optparse import OptionParser  # 명령어 옵션을 처리하기 위한 모듈


# ---------------------------------------------------------
# (1) 백신 에러 처리 클래스 정의
# ---------------------------------------------------------

# 커스텀 예외 클래스: 옵션 파싱 중 에러가 발생하면 예외를 발생시킴
class OptionParsingError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg  # 오류 메시지를 저장


# 프로그램이 특정 옵션에 의해 종료될 때 사용하는 예외 클래스
class OptionParsingExit(Exception):
    def __init__(self, status, msg):
        self.status = status  # 종료 상태 코드 (0: 정상 종료, 1 이상: 오류 종료)
        self.msg = msg  # 오류 메시지 저장


# optparse 모듈의 OptionParser를 확장하여 커스텀 파서를 만듦
class ModifiedOptionParser(OptionParser):
    # 사용자가 잘못된 옵션을 입력하면 예외 발생
    def error(self, msg):
        raise OptionParsingError(msg)

    # 프로그램 종료 시 예외를 발생시켜 처리
    def exit(self, status=0, msg=None):
        raise OptionParsingExit(status, msg)


# ---------------------------------------------------------
# (2) 백신 옵션 정의 함수
# ---------------------------------------------------------

def define_options():
    """
    백신 프로그램에서 사용할 옵션을 정의하는 함수
    """
    usage = "usage: %prog path [options]"  # 사용법 메시지
    parser = ModifiedOptionParser(add_help_option=False, usage=usage)

    # 옵션 정의
    parser.add_option("-f", "--file", action="store_true", dest="opt_file", default=True,
                      help="scan files (default option)")  # 파일 검사 (기본값)
    parser.add_option("-I", "--list", action="store_true", dest="opt_list", default=False,
                      help="list all files in directory")  # 디렉터리 내 파일 목록 출력
    parser.add_option("-V", "--vlist", action="store_true", dest="opt_vlist", default=False,
                      help="list all virus signatures")  # 등록된 바이러스 목록 출력
    parser.add_option("-?", "--help", action="store_true", dest="opt_help", default=False,
                      help="show help")  # 도움말 표시

    return parser  # 설정된 옵션 파서를 반환


# ---------------------------------------------------------
# (3) 백신 옵션 파싱 함수
# ---------------------------------------------------------

def parser_options():
    """
    명령어 입력에서 옵션을 분석하는 함수
    """
    parser = define_options()  # 백신 옵션 정의

    if len(sys.argv) < 2:  # 명령어 입력이 없을 경우
        return 'NONE_OPTION', None  # 아무 옵션도 없음을 반환

    try:
        (options, args) = parser.parse_args()  # 입력된 옵션 분석
        if len(args) == 0:
            return options, None  # 인자가 없는 경우 옵션만 반환
    except OptionParsingError as e:
        return "ILLEGAL_OPTION", e.msg  # 잘못된 옵션이 입력된 경우 처리
    except OptionParsingExit as e:
        return e.status, e.msg  # 프로그램 종료 예외 발생 시 처리

    return options, args  # 정상적으로 옵션과 인자 반환


# ---------------------------------------------------------
# (4) 백신 사용법 출력 함수
# ---------------------------------------------------------

def print_usage():
    """
    프로그램 사용법을 출력하는 함수
    """
    usage_string = """
    Usage:
        python vaccine.py <path> [options]

    Example:
        python vaccine.py C:\\test -f
        python vaccine.py /home/user -I
    """
    print(usage_string)


# ---------------------------------------------------------
# (5) 백신 옵션 설명 출력 함수
# ---------------------------------------------------------

def print_options():
    """
    백신 프로그램에서 사용할 옵션 설명을 출력하는 함수
    """
    options_string = """
    Options:
        -f, --file          Scan files (default option)
        -I, --list          List all files in directory
        -V, --vlist         List all virus signatures
        -?, --help          Show help
    """
    print(options_string)


# ---------------------------------------------------------
# (6) 프로그램의 main() 함수
# ---------------------------------------------------------

def main():
    """
    프로그램의 실행 흐름을 제어하는 main 함수
    """
    options, args = parser_options()  # 옵션을 분석하여 가져옴

    # 프로그램 로고 출력
    print("\n=== Vaccine Scanner v1.0 ===\n")

    # (1) 옵션이 없을 때 기본 사용법과 옵션을 출력
    if options == 'NONE_OPTION':
        print_usage()
        print_options()
        return 0  # 프로그램 종료

    # (2) 잘못된 옵션이 입력된 경우 오류 메시지 출력
    elif options == 'ILLEGAL_OPTION':
        print_usage()
        print("Error: %s is not a valid option" % args)  # 오류 메시지 출력
        return 0  # 프로그램 종료

    # (3) 사용자가 --help 옵션을 입력하면 사용법과 옵션 출력
    if options.opt_help:
        print_usage()
        print_options()
        return 0  # 프로그램 종료

    # TODO: 옵션에 따라 파일 검사, 리스트 출력 등의 기능 구현 필요


# ---------------------------------------------------------
# (7) 프로그램 실행 (entry point)
# ---------------------------------------------------------

if __name__ == '__main__':
    main()  # main() 실행



