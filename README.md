# NPU simulator 만들기

- Python 2차원 리스트와 MAC(Multiply–Accumulate) 연산을 사용해 패턴을 필터와 비교하고 결과를 분석하는 프로그램

## 프로젝트 파일
- main.py: 입력 처리, MAC 연산, 점수 비교, 실행 시간 측정, 모드별 실행 코드

- data.json: 크기별 Cross/X 필터와 테스트 패턴 및 예상 정답

- README.md: 사용법 및 결과 리포트 

## 실행 방법

- **실행 환경**
  - Python 3.9.6
  - macOS 26.2

- **실행 명령어**

```bash
git clone https://github.com/min12252/codyssey_m3_NPU.git
cd codyssey_m3_NPU
python3 main.py
```

## 주요 함수

| 함수 | 역할 | 사용 함수 | 오류 발생시 예외처리
| --- | --- | --- | --- |
| `is_same_size(matrix_a, matrix_b)` | 두 행렬의 NxN 사이즈가 일치하는지 확인 | | 빈 행렬, 2차원 행렬
| `mac(pattern, filter_data)` | 모든 같은위치의 원소를 곱한 뒤 전체 합 점수 반환 | is_same_size() | 행렬의 값이 모두 숫자인지 확인
| `compare_scores(score_a, score_b)` | 점수 차이를 비교해 `A`, `B`, `UNDECIDED` 반환 
| `input_matrix(size)` | 사용자 입력받아 2차원 리스트 생성 | | 값이 숫자인지 확인, 입력 개수 확인
| `measure_time(pattern, filter_data, repeat_count=10)` | MAC 함수 호출 구간을 반복 측정해 평균 ms 반환 | mac() | 반복 횟수 확인
| `normalize_label(label)` | 정규화: `+`를 `Cross`, `x`를 `X`로 변환 | 
| `mode1()` / `mode2()` | 직접 입력 / JSON 일괄 분석 실행 | ALL | -

## MAC 연산과 판정 기준

동일한 크기의 패턴과 필터에 대해 연산을 실행한다
구현은 중첩 `for`문으로 각 위치의 값을 곱해 `total`에 누적하는 방식.

- `abs(score_a - score_b) < 1e-9`이면 `UNDECIDED`로 판정
- `A`점수가 더 높으면 `A`, B 점수가 더 높으면 `B`로 판정

- json 파일 판정 시
  - `+`는 `Cross` / `x`는 `X`로 표준화한 뒤 결과를 비교
  - 실제 판정과 예상 정답이 같으면 PASS, 다르면 FAIL

## 실행 결과
[mod1](log/mod1.txt)

[mod2](log/mod2.txt)

## 실패 원인 및 시간 복잡도 분석

- `size_5_1`은 예상 정답이 X지만 Cross 점수 0.9, X 점수 약 0.9로 거의 같아 `UNDECIDED`
- `size_13_2`는 예상 정답이 Cross지만 두 필터 점수가 모두 약 7.5로 거의 같아 `UNDECIDED`
- `size_25_1`은 예상 정답이 X지만 두 필터 점수가 모두 약 4.9로 거의 같아 `UNDECIDED`
- 세 FAIL 모두 점수 차이가 epsilon(`1e-9`)보다 작아서 발생한 **분류 불확정** 사례이다
- 따라서 이번 FAIL은 MAC 함수가 실행되지 않은 오류가 아니라, 현재의 동점 판정 규칙과 예상 라벨이 일치하지 않아 발생
- 부동소수점 연산에서는 `0.9`와 `0.8999999999999999`처럼 수학적으로 같은 값이 약간 다르게 표현될 수 있다
- epsilon 비교는 이런 작은 표현 차이로 결과를 잘못 선택하는 문제를 줄이기 위한 장치
- 다만 epsilon 범위에 들어오는 사례를 `UNDECIDED`로 처리하기 때문에 예상 정답이 Cross/X이면 FAIL이 될 수 있다
- 각 MAC 연산은 N×N 배열의 모든 위치를 한 번씩 방문하므로 곱셈·누적 연산 횟수는 N²
- 따라서 MAC 연산의 시간 복잡도는 **O(N²)**이며, N이 증가할수록 처리해야 하는 원소 수가 제곱에 비례해 늘어남
- Cross와 X 필터를 모두 계산하므로 패턴당 MAC 연산은 두 번 수행하지만, 상수 배는 점근적 시간 복잡도 O(N²)를 바꾸지 않음
- 실제 실행 시간은 시스템 부하와 측정 오차에 따라 흔들릴 수 있으므로 10회 반복 평균을 사용하고, 단일 측정값만으로 정확한 비례 관계를 단정하지 않는다
