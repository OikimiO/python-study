# 함수
#  - 일급 객체(first-class object)
#  - 일급 객체라는 말은 함수를 직접 참조하고, 변수에 할당하고, 다른 함의 인수로 전달하고
#  - 표현식과 if문 등에서 비교할 수 있다는 의미임

# 튜플을 비교하는 특정한 규칙
#  - 먼저 인덱스 0으로 아이템을 비교히고, 이후 인덱스 1, 인덱스 2로 진행

# 클로저: 자신이 정의된 스코프에 있는 변수를 참조하는 함수
# 튜플: (priority, x)
# 클로저: helper, sort_priority에 정의된 스코프에 있는 변수를 helper가 참조하고 있음

# 파이썬 인터프리터는 참조를 해결하려고 할 때 다음과 같은 순서로 스코프를 탐색
# 1. 현재 함수의 스코프
# 2. 감싸고 있는 스코프
# 3. 코드를 포함하고 있는 모듈의 스코프(전역 스코프)
# 4. (len이나 str같은 함수를 담고 있는) 내장 스코프


# Inner function: local
# Outer function: enclosing
# Global scope: global
# Built-in scope example: 3

x = "global"

def outer_function():
    # 감싸고 있는 스코프 (enclosing scope)
    x = "enclosing"

    def inner_function():
        # 현재 함수의 스코프 (local scope)
        x = "local"
        print("Inner function:", x)  # 'local' 출력

    inner_function()

    # inner_function 바깥에서는 enclosing 스코프 사용
    print("Outer function:", x)  # 'enclosing' 출력


outer_function()

# 전역 스코프 사용
print("Global scope:", x)  # 'global' 출력

# 내장 스코프 예제 (built-in scope)
print("Built-in scope example:", len([1, 2, 3]))  # 내장 함수 len 사용

# 참조를 해결하는 예제
# 헬퍼 함수 + 클로저: group에 속하는 값을 우선순위로 정렬하고, 이후 다음 우선 순위를 정렬
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0,x) # x in group, (priority, x)
        return (1,x)  # x not in group, (priority, x)
    # 튜플의 첫번째 요소를 기준으로 정렬
    # 이후에 튜플의 두번째 요소를 기준으로 정렬
    values.sort(key=helper)

# [2, 3, 5, 7, 1, 4, 6, 8]
numbers = [8,3,1,2,5,4,7,6]
group = [2,3,5,7]
sort_priority(numbers, group)
print(numbers)

numbers = [8,3,1,2,5,4,7,6]
group = [2,3,5,7]

# 헬퍼 함수 + 클로저: group에 속하는 값을 우선순위로 정렬하고, 이후 다음 우선 순위를 정렬
# 만약 numbers가 group의 숫자에 포함되면 True를 반환
# 하지만 다음의 방법으로는 True를 반환하지 않음
# 왜? sort_priority2에 선언된 found는 입력을 할 때는 반드시 자신의 스코프에서만 변화를 줘야 함
#     helper에서는 found라는 변수가 새로운 변수로 인식됨
def sort_priority2(numbers, group):
    found = False # 스코프: sort_priority2
    def helper(x):
        if x in group:
            found = True # 스코프: helper
            return (0,x)
        return (1,x)
    numbers.sort(key=helper)
    return found

# found: False
# [2, 3, 5, 7, 1, 4, 6, 8]
found = sort_priority2(numbers, group)
print('found: %s' %found)
print(numbers)

numbers = [8,3,1,2,5,4,7,6]
group = [2,3,5,7]

# 헬퍼 함수 + 클로저: group에 속하는 값을 우선순위로 정렬하고, 이후 다음 우선 순위를 정렬
# 만약 numbers가 group의 숫자에 포함되면 True를 반환
# 단점: nonlocal을 이용한 방식은 유지 보수를 어렵게 만듦
def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0,x)
        return (1,x)
    numbers.sort(key=helper)
    return found

# found: True
# [2, 3, 5, 7, 1, 4, 6, 8]
found = sort_priority3(numbers, group)
print('found: %s' %found)
print(numbers)

numbers = [8,3,1,2,5,4,7,6]
group = [2,3,5,7]

# 클래스: group에 속하는 값을 우선순위로 정렬하고, 이후 다음 우선 순위를 정렬
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)   # __init__: Sorter class에 group이 입력
numbers.sort(key=sorter) # __call__: 현재 객체 중 함수처럼 사용된 sorter를 호출할 때 실행
assert sorter.found is True

numbers = [8,3,1,2,5,4,7,6]
group = [2,3,5,7]

# 헬퍼 함수 + 클로저: group에 속하는 값을 우선순위로 정렬하고, 이후 다음 우선 순위를 정렬
# 만약 numbers가 group의 숫자에 포함되면 True를 반환
#  - dictionary, set을 이용하면 부모 스코프의 변수를 변경할 수 있음
def sort_priority4(group, numbers):
    found = [False]
    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

found = sort_priority4(group, numbers)
print(found)