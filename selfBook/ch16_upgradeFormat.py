# 백신 커널 및 플러그인 엔진 테스트를 위해서는, 다양한 파일에 대한 검사가 가능해야 함 -> 권한 & 파일 포멧
## ex: zipfile 모듈을 이용하면, zip 파일 압축 및 해제가 가능함
### 이전에 작성한 플러그인 백신 엔진 구조는 아래와 같다.
#### - 아래 -
#### [1. init, 2. uninit, 3.scan, 4. disinfect, 5. listvirus 6. getinfo] < 하나의 클래스 : KavMain
import zipfile


##### => 기존 엔진의 scan 함수만으로는 압축 파일 내부에 존재하는 악성코드를 검사할 수 없다. (file)

###### => 함수 보강 [ 7. format / 8. arclist / 9. unarc ]

import zipfile  # ZIP 파일을 다루기 위한 모듈
import os  # 파일 조작을 위한 모듈
import shutil  # 파일 복사 및 이동을 위한 모듈


class ForFileFormat:
    """
    다양한 파일 포맷을 분석하고, 압축 파일 내부의 파일 목록을 추출하며,
    특정 파일을 압축 해제하는 기능을 제공하는 클래스
    """

    def format(self, filehandle, filename):
        """
        파일의 포맷을 분석하는 함수.
        특정한 파일 포맷(예: ZIP)을 판별하여 관련 정보를 저장함.

        :param filehandle: 메모리에 로드된 파일 데이터 (mmap 등 사용 가능)
        :param filename: 파일의 이름 (사용되지 않지만 확장 가능성 고려)
        :return: ZIP 파일이라면 {'ff_zip': format} 반환, 아니라면 None 반환
        """
        fileformat = {}  # 포맷 정보를 저장할 딕셔너리

        mm = filehandle  # 파일 내용을 가리키는 변수

        # ZIP 파일의 헤더는 'PK\x03\x04' 로 시작하므로 이를 확인
        if mm[0:4] == b'PK\x03\x04':  # ZIP 파일의 마법 숫자 (Magic Number)
            fileformat['size'] = len(mm)  # 파일 크기 정보 저장

            # ZIP 포맷임을 나타내는 정보 반환
            ret = {'ff_zip': fileformat}
            return ret

        return None  # ZIP 파일이 아닌 경우 None 반환

    def arclist(self, filename, fileformat):
        """
        압축 파일 내부의 파일 목록을 얻는 함수.

        :param filename: 분석할 압축 파일의 경로
        :param fileformat: 미리 분석된 파일 포맷 정보
        :return: 압축 파일 내부의 파일 목록을 담은 리스트
                 리스트 요소 형식: ['arc_zip', 파일명]
        """
        file_scan_list = []  # 검사 대상 파일 목록 저장

        # 미리 분석된 파일 포맷 중 ZIP 포맷이 존재하는지 확인
        if 'ff_zip' in fileformat:
            zfile = zipfile.ZipFile(filename)  # ZIP 파일 열기

            # 압축 파일 내부의 파일명들을 가져와 리스트에 추가
            for name in zfile.namelist():
                file_scan_list.append(['arc_zip', name])

            zfile.close()  # ZIP 파일 닫기 (자원 해제)

        return file_scan_list  # 압축 파일 내의 파일 목록 반환

    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        """
        압축 파일 내부의 특정 파일을 압축 해제하는 함수.

        :param arc_engine_id: 압축 파일의 엔진 식별자 ('arc_zip' 등)
        :param arc_name: 압축 파일의 경로
        :param fname_in_arc: 압축 파일 내부에서 해제할 파일의 이름
        :return: 압축 해제된 파일의 바이너리 데이터 (str 또는 bytes 형식)
        """
        if arc_engine_id == 'arc_zip':  # ZIP 파일인지 확인
            zfile = zipfile.ZipFile(arc_name)  # ZIP 파일 열기
            data = zfile.read(fname_in_arc)  # 특정 파일 압축 해제 및 데이터 읽기
            zfile.close()  # ZIP 파일 닫기

            return data  # 압축 해제된 데이터 반환

        return None  # 지원되지 않는 압축 형식의 경우 None 반환

    def disinfect_and_repack(self, zip_path, infected_files):
        """
        악성코드가 포함된 파일을 삭제한 후 ZIP 파일을 재압축하는 함수.

        :param zip_path: 원본 ZIP 파일 경로
        :param infected_files: 삭제할 악성코드 파일 리스트
        """
        temp_dir = "temp_zip_extract"  # 압축 해제할 임시 디렉터리

        # 기존 압축 해제 폴더가 있으면 삭제 후 새로 생성
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        # ZIP 파일 압축 해제
        with zipfile.ZipFile(zip_path, 'r') as zfile:
            zfile.extractall(temp_dir)

        # 악성 파일 삭제
        for infected_file in infected_files:
            infected_path = os.path.join(temp_dir, infected_file)
            if os.path.exists(infected_path):
                os.remove(infected_path)

        # 새 ZIP 파일 생성 (덮어쓰기)
        new_zip_path = zip_path  # 기존 ZIP 파일을 덮어씀
        with zipfile.ZipFile(new_zip_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    new_zip.write(file_path, arcname)

        # 임시 디렉터리 삭제
        shutil.rmtree(temp_dir)

        print(f"ZIP 파일이 재압축되었습니다: {new_zip_path}")

# 파일 입출력이 빈번하게 일어날 수록 속도는 느려진다 -> I/O 를 최소화 해야함
# 01 모든 파일을 한꺼번에 압축 해제하게 되면 파일 입출력은 줄어든다 -> 단 한번의 분석으로 모든 파일을 압축 해제
# 02 모든 파일을 한개씩 합축 해제한 뒤 악성코드를 검사하게 되면, 저장 공간을 많이 차지하지는 않지만 파일 I/O가 증가함

# if, 악성코드가 존재한다면? -> zip 파일을 압축 해제하고 / 해당 악성코드 파일을 삭제한 다음  -> ZIP 파일은 재압축 되어야 한다.
## 한글 파일& PDF 파일도 똑같다 풀고, 마스킹 또는 검출 -> 그 후 다시 압축