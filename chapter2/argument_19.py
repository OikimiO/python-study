# 함수의 인수를 위치나 키워드로 지정할 수 있다.
# 위치 인수만 으로는 이해하기 어려울 때 키워드 인수를 쓰면 각 인수를 사용하는 목적이 명확해진다.
# 키워드 인수에 기본값을 지정하면 함수에 새 동작을 쉽게 추가할 수 있다.
#  - 특히, 함수를 호출하는 기존코드가 있을 때 사용하면 좋다
# 선택적인 키워드 인수는 항상 위치가 아닌 키워드로 넘겨야 한다.

def ramainder(number, divisor):
    return number % divisor

assert ramainder(20, 7) == 6
#remainder(20, divisor=7) == 6
#assert remainder(number=20, divisor=7) == 6
#assert remainder(divisor=7, number=20) == 6

def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3

# 0.167 kg per second
flow = flow_rate(weight_diff, time_diff)
print('%.3f kg per second' % flow)

def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period

# 0.16666666666666666
flow_per_second = flow_rate(weight_diff, time_diff, 1)
print(flow_per_second)

# 헬퍼 함수: (weight_diff / time_diff) * period를 구하되 period의 기본값을 1로 설정
# 선택적 인수를 추가해 default설정이 가능
# 다음 선택적 인수는 간단한 인수에는 잘 작동하지만 복잡한 방식엔 잘 동작하지 않음
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period

# 0.16666666666666666
flow_per_second = flow_rate(weight_diff, time_diff)
print(flow_per_second)

# 600.0
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
print(flow_per_hour)

def flow_rate(weight_diff, time_diff, period=1, unit_per_kg = 1):
    return ((weight_diff / unit_per_kg) / time_diff) * period

# 272.72727272727275
pounds_per_hour = flow_rate(weight_diff, time_diff, period=3600, unit_per_kg=2.2)
print(pounds_per_hour)