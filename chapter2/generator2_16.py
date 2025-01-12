from itertools import islice

# 헬퍼 함수 + 일반 루프: 공백(" ")을 구분자로 해서 0~2번째 문자의 첫번째 인덱스를 출력
# 단점
#  1. 코드가 복잡하고 깔끔하지 않음
#  2. 모든 결과를 리스트에 저장
def index_word(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

address = 'Four score and seven years ago...'
result = index_word(address)
# [0, 5, 11]
print(result[:3])

# 헬퍼 함수 + 제너레이터 함수: 공백(" ")을 구분자로 해서 0~2번째 문자의 첫번째 인덱스를 출력
# 1번 단점을 해결
def index_word_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

# 0
# 5
# 11
temp = index_word_iter(address)
print(next(temp))
print(next(temp))
print(next(temp))

# 헬퍼 함수 + 제너레이터 함수: 공백(" ")을 구분자로 해서 0~2번째 문자의 첫번째 인덱스를 출력
# 제너레이터는 기본적으로 게으르게(=lazy) 값을 생성함
# 그래서, 배열을 바로 만들지 않고 현재 작업만 진행함
# 단, 이전 상태를 기억해 다음에 작업을 진행할 때는 참조를 함
# 이런 특징때문에 제너레이터는 큰 파일의 용량도 효율적으로 처리할 수 있음
# 결론적으로 2번 단점을 해결
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

with open("../tmp/address.txt","r") as f:
    it = index_file(f)
    results = islice(it,0,3)
    print(list(results))