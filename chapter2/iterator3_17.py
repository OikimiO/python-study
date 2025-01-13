path = "../tmp/my_numbers.txt"

# 헬퍼 함수: 방문자 수 / 방문자 배열의 합를 배열로 출력
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# [11.538461538461538, 26.923076923076923, 61.53846153846154]
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

# 해당 결과가 나온 것은 이터레이터가 결과를 한번만 생성하기 떄문
# []
it = read_visits(path)
percentages = normalize(it)
print(percentages)

# [15, 35, 80]
# []
it = read_visits(path)
print(list(it))
print(list(it)) # 이미 소진

# 헬퍼 함수: 방문자 수 / 방문자 배열의 합를 배열로 출력
# 위의 빈 배열([])이 나왔던 문제를 해결하기 위해 입력 이터레이터를 명시적으로 소진 - list(numbers)
# 전체 컨텐츠의 복사본을 리스트에 저장하여 사용
# 단점: 매번 새 배열을 선언 해 매모리 사용량이 높음
def normalize_copy(numbers):
    numbers = list(numbers)
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# [11.538461538461538, 26.923076923076923, 61.53846153846154]
it = read_visits(path)
percentages = normalize_copy(it)
print(percentages)

# 헬퍼 함수: 방문자 수 / 방문자 배열의 합를 배열로 출력
# 매번 새 이터레이터를 호출하여 메모리 사용량을 줄임
# 단점: lambda를 이용한 방법이 가독성이 없음
def normalize_func(get_iter):
    total = sum(get_iter()) # 새 이터레이터
    result = []
    for value in get_iter(): # 새 이터레이터
        percent = 100 * value / total
        result.append(percent)
    return result

# [11.538461538461538, 26.923076923076923, 61.53846153846154]
percentages = normalize_func(lambda: read_visits(path))
print(percentages)

class ReadVisits(object):
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

# [11.538461538461538, 26.923076923076923, 61.53846153846154]
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)

def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers):
        raise TypeError('Must supply a container') # 이터레이터 -- 거부!
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# [11.538461538461538, 26.923076923076923, 61.53846153846154]
visits = [15, 35, 80]
percentages = normalize_defensive(visits) # 오류 없음
print(percentages)

# [11.538461538461538, 26.923076923076923, 61.53846153846154]
visits = ReadVisits(path)
percentages = normalize_defensive(visits) # 오류 없음
print(percentages)

it = iter(visits)
normalize_defensive(it)
