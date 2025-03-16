# 안티 바이러스 엔진이 제대로 동작하는가를 체크하기 위하여 고안한 가짜 바이러스
# X5O! 중략 -ANTIVIRUS-TEST-FILE

import hashlib
import os

fp = open('ericar.txt', 'rb') # 바이너리 모드로 읽는다. (텍스트 모드로 읽지 않는 이유는 악성코드 문자열의 다양성 고려)
fbuf = fp.read()
fp.close()

m_is_for_compare = hashlib.md5()
m_is_for_compare.update(fbuf)
fmd5 = m_is_for_compare.hexdigest()

# Eicar test 파일 MD5와 비교
if fmd5 == '*임의 특정한 해쉬값 ex: 44d888612fea' :
    print("This is Virus")
    os.remove('ericar.txt') # 바이러스가 맞다면 파일을 삭제해서 치료 (백신 default 알고리즘)
else :
    print("This is Not Virus")


# 전용 백신 배포본 만들기
# 8.1 Pyinstaller
#   - 파이썬으로 작성된 소스코드를 윈도우 실행파일로 변환 [.py -> .exe]
# (사용법) 해당 파이썬 소스코드가 존재하는 폴더로 이동한다. 그 다음 명령어를 입력한다. -> dist 폴더에 실행파일 생성