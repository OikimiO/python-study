"""
    # CPU 병목점을 C 확장 모듈로 옮기는 방법은 파이썬 코드에 최대한 투자하면서 성능을
      개선할 수 있는 효과적인 방법이다. 하지만 이렇게 하면 비용이 많이 들어가고 버그가 생길 수도 있다.
    # multiprocessing 모듈은 파이썬에서 특정 유형의 계산을 최소화한 노력으로 병렬화할 수 있는
      강력한 도구를 제공한다.
    # multiprocessing의 강력한 기능은 concurrent.futures와 그 안에 들어있는 간단한
      ProcessPoolExecutor 클래스로 접근하는 것이 좋다.
    # multiprocessing 모듈의 고급 기능은 너무 복잡하므로 피하는 것이 좋다
"""
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from time import time


def gcd(pair):
    a,b = pair
    low = min(a,b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

numbers = [(1963309, 2265973), (2030677, 3814172),
           (1551645, 2229620), (2039045, 2020802)]

#start = time()
#results = list(map(gcd, numbers))
#end = time()
# Took 0.199 seconds
#print('Took %.3f seconds'%(end-start))

# 오류 발생..
start = time()
# pool = ThreadPoolExecutor(max_workers=2)
pool = ProcessPoolExecutor(max_workers=2)
results = list(pool.map(gcd, numbers))
end = time()
print('Took %.3f seconds'%(end-start))