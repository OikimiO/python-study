"""
    # 데코레이터는 런타임에 한 함수로 다른 함수를 수정할 수 있게 파이썬 문법이다.
    # 데코레이터를 사용하면 디버거와 같이 객체 내부를 조사하는 도구가 이상하게 동작할 수도 있다.
    # 직접 데코레이터를 정의할 때 이런 문제를 피하려면 내장 모듈 functools의 wraps 데코레이터를 사용하자
"""
from functools import wraps

def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' % (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace
def fibonacci(n):
    """n번째 피보나치 수를 반환한다"""
    if n in (0,1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

fibonacci = trace(fibonacci)
# fibonacci((1,), {}) -> 1
# wrapper((1,), {}) -> 1
# fibonacci((0,), {}) -> 0
# wrapper((0,), {}) -> 0
# fibonacci((1,), {}) -> 1
# wrapper((1,), {}) -> 1
# fibonacci((2,), {}) -> 1
# wrapper((2,), {}) -> 1
# fibonacci((3,), {}) -> 2
# wrapper((3,), {}) -> 2
fibonacci(3)

# <function trace.<locals>.wrapper at 0x1041b0a60>
print(fibonacci)

help(fibonacci)

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' % (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace
def fibonacci(n):
    """n번째 피보나치 수를 반환한다"""
    if n in (0,1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

# fibonacci(n)
#     n번째 피보나치 수를 반환한다
help(fibonacci)