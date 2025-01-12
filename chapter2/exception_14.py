# 헬퍼 함수: 분모를 0으로 나누었을 때, Invalid inputs를 출력
# None
# Invalid inputs
def divide(a,b):
    try:
        return a/b
    except ZeroDivisionError:
        return None

result = divide(4,0)
print(result)
if result is None:
    print("Invalid inputs")

# 다음은 분모가 0인 경우가 Invalid inputs를 출력해야하는데 분자가 0인 경우도
# 0.0 > not 0.0 = not False = True
# Invalid inputs
result = divide(0,5)
print(result)
if not result:
    print("Invalid inputs")

# 헬퍼 함수: return에 계산된 결과일 경우는 True, 계산 결과를 아닐 경우는 False, None을 리턴
# 단점: 파이썬은 사용하지 않는 변수에 밑줄(_)을 사용하는 관례가 있어
# 다음의 코드는 None을 반환하는 것 만큼 나쁨
def divide(a,b):
    try:
        return True, a/b
    except ZeroDivisionError:
        return False, None

#
success, result = divide(0,5)
if not success:
    print("Invalid inputs")

# 해당 헬퍼 함수의 이해가 없는 개발자는 실수할 확률을 높임
# Invalid inputs
_, result = divide(0,5)
if not result:
    print("Invalid inputs")

# 헬퍼 함수: 계산된 결과는 a/b로 출력, 분모를 0으로 나눈 경우 except처리(ValueError)
def divide(a,b):
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

# Result is 2.5
try:
    result = divide(5,2)
except:
    print("Invalid inputs")
else:
    print("Result is %.1f" % result)

# Invalid inputs
try:
    result = divide(5,0)
except:
    print("Invalid inputs")
else:
    print("Result is %.1f" % result)