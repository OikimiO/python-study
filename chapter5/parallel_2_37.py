"""
    # 파이썬 스레드는 전역 인터프리터 잠금(GIL, Global Interpreter Lock) 때문에 여러 CPU 코어에서
      병렬로 바이트 코드를 실행할 수 없다.
    # GIL에도 불구하고 파이썬 스레드는 동시에 여러 작업을 하는 것처럼 보여주기 쉽게 해주므로 여전히 유용하다
    # 여러 시스템 호출을 병렬로 수행하려면 파이썬 스레드를 사용하자. 이렇게 하면 계산을 하면서도 블로킹 I/O
      를 수행할 수 있다.
"""
from time import time
from threading import Thread
import select

def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

numbers = [2139079, 1213759, 1516637, 1852285]
start = time()
for number in numbers:
    list(factorize(number))
end = time()
# Took 0.253 seconds
print('Took %.3f seconds' % (end - start))

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

start = time()
threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
end = time()
# Took 0.234 seconds
print('Took %.3f seconds' % (end - start))

def slow_systemcall():
    select.select([],[],[],0.1)

start = time()
for _ in range(5):
    slow_systemcall()
end = time()
# Took 0.511 seconds
print('Took %.3f seconds' % (end - start))

start = time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall())
    thread.start()
    threads.append(thread)

def compute_helicopter_location(index):
    # ...
    return index

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()
end = time()
# Took 0.522 seconds ... 흠.. 이게 이전 작업보다 빠르다는데 현재 결과는 더 느림..
print('Took %.3f seconds' % (end - start))