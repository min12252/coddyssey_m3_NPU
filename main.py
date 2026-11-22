import time
import json


# 크기 비교
def is_same_size(matrix_a, matrix_b):
    # 빈 행렬 확인
    if not matrix_a or not matrix_b:
        raise ValueError("빈 행렬은 사용할 수 없습니다.")

    # 행 개수 비교
    if len(matrix_a) != len(matrix_b):
        raise ValueError("행렬의 행 수가 다릅니다.")

    # 각 행이 리스트인지 확인
    for i in range(len(matrix_a)):
        if not isinstance(matrix_a[i], list) or not isinstance(matrix_b[i], list):
            raise ValueError("2차원 행렬을 입력해야 합니다.")

        # 열 개수 비교
        if len(matrix_a[i]) != len(matrix_b[i]):
            raise ValueError("행렬의 열 수가 다릅니다.")

    return True


# MAC 연산 수행
def mac(pattern, filter_data):
    ## 입력 배열과 필터 배열이 비어있는지 확인
    if not pattern or not filter_data:
        raise ValueError("빈 배열은 사용할 수 없습니다.")

    ## 배열 크기 확인
    if not is_same_size(pattern, filter_data):
        raise ValueError("같은 크기의 배열을 입력해야 합니다.")
    
    ## 누적 합 초기화
    total = 0

    ## 배열 순회
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            if not isinstance(pattern[i][j], (int, float)) or not isinstance(filter_data[i][j], (int, float)):
                raise ValueError("행렬의 요소는 숫자여야 합니다.")
            # 같은 위치의 값 곱하기
            result = pattern[i][j] * filter_data[i][j]
            # 결과 누적
            total += result
    
    ## 최종 점수 반환
    return total


# 점수 비교
def compare_scores(score_a, score_b):
    if abs(score_a - score_b) < 1e-9:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"


# 사용자로부터 행렬 입력 받기
def input_matrix(size: int):

    pattern = []

    print(f"{size}×{size} 행렬을 입력하세요. 각 행의 숫자는 공백으로 구분합니다.")

    for i in range(size):
        while True:
            user_input = input(f"{i + 1}번째 행의 숫자 {size}개를 입력하세요: ")
            try:
                row = list(map(int, user_input.split()))
            except ValueError:
                print("숫자만 입력해야 합니다.")
                continue

            if len(row) != size:
                print(f"숫자를 정확히 {size}개 입력해야 합니다.")
            else:
                pattern.append(row)
                break
    return pattern


# 평균 연산 시간 측정
def measure_time(pattern, filter_data, repeat_count=10):

    if repeat_count <= 0:
        raise ValueError("반복 횟수는 1 이상이어야 합니다.")

    total_time = 0

    for i in range(repeat_count):
        start = time.perf_counter()
        mac(pattern, filter_data)
        end = time.perf_counter()
        total_time += (end - start) * 1000

    average_time = total_time / repeat_count
    return average_time


# 라벨 표준화(정규화)
def normalize_label(label):
    if label == "+":
        return "Cross"
    elif label == "x":
        return "X"
    else:
        return label


# 모드 1: 사용자 직접 입력
def mode1():
    ## 사용자 입력 받기
    print("패턴을 입력하세요.")
    pattern = input_matrix(3)

    print("필터 A를 입력하세요.")
    filter_a = input_matrix(3)

    print("필터 B를 입력하세요.")
    filter_b = input_matrix(3)

    ## MAC 연산 수행 및 시간 측정
    score_a = None
    score_b = None
    average_time_a = None
    average_time_b = None
    try:
        ### MAC 연산 수행
        score_a = mac(pattern, filter_a)
        score_b = mac(pattern, filter_b)
        print("score_a 점수:", score_a)
        print("score_b 점수:", score_b)
        ### 연산 시간 측정
        average_time_a = measure_time(pattern, filter_a)
        average_time_b = measure_time(pattern, filter_b)
        print("score_a 평균 연산 시간:", average_time_a, "ms")
        print("score_b 평균 연산 시간:", average_time_b, "ms")
    except ValueError as e:
        print("ERROR:", e)

    ## 점수 비교
    if score_a is not None and score_b is not None:
        result = compare_scores(score_a, score_b)

        if result == "UNDECIDED":
            print("두 필터의 점수가 같습니다.")
        elif result == "A":
            print("A 필터의 점수가 더 높습니다.")
        else:
            print("B 필터의 점수가 더 높습니다.")


# 모드 2: JSON 파일 사용
def mode2():
    ## JSON 데이터 불러오기
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    ## 필터와 패턴 데이터 분리
    filters = data["filters"]
    patterns = data["patterns"]

    ## 개수 집계 초기화
    total_count = 0
    pass_count = 0
    fail_count = 0

    # 크기별 성능 측정 결과 저장
    performance = {}

    ## 패턴별 데이터 가져오기
    for pattern_name in patterns.keys():
        ### 패턴 이름에서 행렬 크기 추출
        parts = pattern_name.split("_")
        size = int(parts[1])

        ### 패턴 데이터 가져오기
        pattern_data = patterns[pattern_name]["input"]

        ### 행렬 크기에 맞는 필터 선택
        selected_filter = filters[f"size_{size}"]

        ### Cross, X 필터 가져오기
        filter_cross = selected_filter["cross"]
        filter_x = selected_filter["x"]

        try:
            ### MAC 연산
            score_cross = mac(pattern_data, filter_cross)
            score_x = mac(pattern_data, filter_x)

            ### 시간 측정
            average_time_cross = measure_time(pattern_data, filter_cross)
            average_time_x = measure_time(pattern_data, filter_x)

            ### 크기별 평균 측정시간 저장
            if size not in performance:
                performance[size] = []

            performance[size].append((average_time_cross + average_time_x) / 2)

            ### 점수 비교
            result = compare_scores(score_cross, score_x)
            if result == "A":
                result = "Cross"
            elif result == "B":
                result = "X"

            ### 예상 결과값 표준화
            expected = normalize_label(patterns[pattern_name]["expected"])

            ### 결과 집계
            total_count += 1

            if result == expected:
                pass_count += 1
                status = "PASS"
            else:
                fail_count += 1
                status = "FAIL"

            ### 결과 출력    
            print(f"{total_count}. {pattern_name}")
    
            print(f"size: {size}×{size}")
            print("예상:", expected)
            print(f"연산 평균 시간 (10회): Cross={average_time_cross:.6f}ms, X={average_time_x:.6f}ms")
            print(f"점수: Cross={score_cross}, X={score_x}")
            print("판정:", result)
            print("결과:", status)
            print("--------------------")

        except ValueError as e:
                    print("ERROR:", e)
    

    ## 결과 출력
    print("[total]")
    print("전체 패턴 수:", total_count)
    print("PASS:", pass_count)
    print("FAIL:", fail_count)
    print("크기별 평균 연산 시간:")
    for size, times in performance.items():
        average_time = sum(times) / len(times)
        print(f"{size}×{size}: {average_time:.6f} ms")
        

### 메인 실행 부분 ###
mode = input("모드를 선택하세요 (1 또는 2): ")

if mode == "1":
    mode1()
elif mode == "2":
    mode2()
else:
    print("올바른 모드를 선택하세요.")