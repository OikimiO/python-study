# 파이썬에서 컴포넌트 사이에 간단한 인터페이스용으로 클래스를 정의하고 인스턴스를 생성하는 대신에 함수만 써도 종종 충분하다
# 파이썬에서 함수와 메서드에 대한 참조는 일급이다. 즉, 다른 타입처럼 표현식에서 사용할 수 있다.
# __call__ 이라는 특별한 메서드는 클래스의 인스턴스를 일반 파이썬 함수처럼 호출할 수 있게 해준다.
# 상태를 보존하는 함수가 필요할 때 상태 보존 클로저를 정의하는 대신 __call__메서드를 제공하는 클래스를 정의하는 방안을 고려하자

from collections import defaultdict

names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
# 람다 + 정렬: 문자 원소 중 길이가 긴 데이터부터 정렬하여 출력 
names.sort(key=lambda x: len(x))
print(names)

def log_missing():
    print('Key added')
    return 0 # int의 기본 값

current = {'green': 12, 'blue':13}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9)    
]

result = defaultdict(log_missing, current) # value의 타입, 
# Before: {'green': 12, 'blue': 13}
# Key added
# Key added
# After:  {'green': 12, 'blue': 30, 'red': 5, 'orange': 9}
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After: ', dict(result))

# 장점: 간단한 함수를 인터페이스용으로 사용할 때 클로저 안에 상태를 숨기면 나중에 기능을 추가하기 쉬움
# 단점: 클로저 안에 상태 보존을 하기에 코드를 이해하기 어려움
def increment_with_report(current, increments):
    added_count = 0
    
    def missing():
        nonlocal added_count # 상태 보존 클로저, 내부 함수에서 외부 함수의 변수를 변경할 때 사용
        added_count += 1
        return 0
    
    result = defaultdict(missing, current)
    for key, amount in increments:
        # print(result[key]) 
        result[key] += amount
    
    return result, added_count

result, count = increment_with_report(current, increments)
assert count == 2

# 클래스:메서드 후킹을 통해 counter.added의 값을 2 출력
# 장점: 앞서 상태 보존 클로저의 동작보다 명확함
class CountMissing(object):
    def __init__(self):
        self.added = 0
    
    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter.missing, current) # 메서드 참조

for key, amount in increments:
    result[key] += amount

assert counter.added == 2

# __call__을 통해 후크의 용도를 좀 더 명확히 알려줄 수 있음
class BetterCountMissing(object):
    def __init__(self):
        self.added = 0
    
    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
counter()
assert callable(counter) # True 반환

# CountMissing.missing 예제보다 더 명확함
# __call__ 메서드는 (API 후크처럼) 함수 인수를 사용하기 적합한 위치에 클래스의 인스턴스를 사용
# 할 수 있다는 것을 보여줌
counter = BetterCountMissing()
result = defaultdict(counter, current) # __call__이 필요함
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
