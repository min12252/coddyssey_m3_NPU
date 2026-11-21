

# for row in pattern:
#     for value in row:
#         print(value, end=" ")

# print("인덱스로 배열 순회")

# for i in range(3):
#     for j in range(3):
#         print(f"위치: [{i}][{j}], 값: {pattern[i][j]}")

pattern = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

filter_a = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

pattern_5 = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1]
]

filter_5 = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1]
]
# total = 0

# for i in range(3):
#     for j in range(3):
#         result = pattern[i][j] * filter_a[i][j]
#         total = total + result

# print("MAC 점수:", total)

def mac(pattern, filter_data):
    # 누적 합 초기화
    total = 0

    # 배열 순회
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            # 같은 위치의 값 곱하기
            result = pattern[i][j] * filter_data[i][j]
            # 결과 누적
            total += result
    
    # 최종 점수 반환
    return total

score_3 = mac(pattern, filter_a)
print("MAC 점수:", score_3)

score_5 = mac(pattern_5, filter_5)
print("5×5 MAC 점수:", score_5)

if abs(score_3 - score_5) < 1e-9:
    print("UNDECIDED")
elif score_3 > score_5:
    print("score 3의 점수가 더 큽니다.")
else:
    print("score 5의 점수가 더 큽니다.")

pattern = []

for i in range(3):
    row = input(f"{i+1}번째 행을 입력하세요: ")
    numbers = list(map(int,row.split()))
    while len(numbers) != 3:
        print("3개의 숫자를 입력해야 합니다.")
        row = input(f"{i+1}번째 행을 입력하세요: ")
        try:
            numbers = list(map(int,row.split()))
        except ValueError:
            print("숫자만 입력해야 합니다.")
            continue

    pattern.append(numbers)

print(pattern)