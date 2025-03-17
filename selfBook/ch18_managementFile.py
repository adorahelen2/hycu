import hashlib

# 파일 정보 저장을 위한 구조체 역할 (딕셔너리 활용)
# 💡 개념 정리: 검사 완료 후 update_info 에 추가하는 이유
#
# 1️⃣ 악성코드 검사가 완료됨
# 	•	백신 엔진이 ZIP, EXE, PDF 등 다양한 파일을 검사한다고 가정
# 	•	특정 파일을 검사한 후 악성코드가 존재하는지 여부를 판단
#
# 2️⃣ 파일 정보 구조체 (update_info)란?
# 	•	검사한 파일의 정보(예: 파일명, 검사 결과, 검사 시각 등)를 저장하는 구조체
# 	•	파일이 재검사가 필요한지, 감염되었는지, 치료되었는지를 추적
#
# 3️⃣ 갱신 여부를 체크하는 이유
# 	•	한 번 검사한 파일을 다시 검사할 필요가 있을까?
# 	•	예를 들어, 같은 파일을 또 검사하는 비효율을 막기 위해 “이 파일은 검사 완료됨”이라고 표시할 필요가 있음
# 	•	즉, update_info에 검사 정보를 추가하여, 파일이 변경되었거나 새로운 파일일 때만 다시 검사

# ✔ update_info에 검사 결과 저장
# ✔ 파일 해시(SHA-256)를 활용하여 변경 여부 확인
# ✔ 이미 검사한 파일이면 다시 검사하지 않음


update_info = {}


def calculate_hash(filename):
    """파일의 SHA-256 해시를 계산하여 변조 여부 확인"""
    hasher = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_file(filename):
    """파일을 검사하고, 결과를 update_info에 추가"""

    file_hash = calculate_hash(filename)

    # 이미 검사한 파일인지 확인
    if filename in update_info:
        if update_info[filename]["hash"] == file_hash:
            print(f"[✔] {filename}: 이미 검사 완료된 파일 (변경 없음)")
            return

    # 악성코드 여부 검사 (예제에서는 특정 문자열 포함 여부로 간단히 처리)
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    is_malicious = "malware" in content  # 실제로는 정교한 분석 필요

    # 검사 결과를 update_info에 추가
    update_info[filename] = {
        "hash": file_hash,
        "is_malicious": is_malicious
    }

    # 검사 결과 출력
    if is_malicious:
        print(f"[⚠] {filename}: 악성코드 발견!")
    else:
        print(f"[✔] {filename}: 안전한 파일")


# 테스트 실행
scan_file("test1.txt")  # 검사 실행
scan_file("test1.txt")  # 변경 없으면 다시 검사 안 함