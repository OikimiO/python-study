# 키워드 인수는 함수 호출의 의도를 더 명확하게 해준다.
# 특히 불 블래그를 여러개 받는 함수처럼 헷갈리기 쉬운 함수를 호출할 때 키워드 인수를
# 넘기게 하려면 키워드 전용 인수를 사용하자
# 파이썬3는 함수의 키워드 전용 인수 문법을 명시적으로 지원한다.
# 파이썬 2에서는 **kwargs를 사용하고 TypeError예외를 직접 일으키는 방법으로 함수의
# 키워드 전용 인수를 흉내 낼 수 있다.
def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# 0.0
result = safe_division(1, 10**500, True, False)
print(result)

# inf
result = safe_division(1, 0, False, True)
print(result)

def safe_division_b(number, divisor,
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

safe_division_b(1, 10 ** 500, ignore_overflow= True)
safe_division_b(1, 10 ** 500, ignore_zero_division= True)
safe_division_b(1, 10 ** 500, True, False)

# *를 사용하면 위치 인수는 사용할 수 없고, 키워드 인수만 사용할 수 있음
def safe_division_c(number, divisor, *,
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# safe_division_c() takes 2 positional arguments but 4 were given
#safe_division_c(1, 10 ** 500, True, False)

safe_division_c(1, 10 ** 500, ignore_zero_division=True)

try:
    safe_division_c(1, 0)
except ZeroDivisionError:
    pass # 기대한 대로 동작함