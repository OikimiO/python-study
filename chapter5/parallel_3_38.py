"""
    # 파이썬에 전역 인터프리터 잠금이 있다고 해도 프로그램 안에서 실행되는 스레드간의
      데이터 경쟁으로부터 보호할 책임은 프로그래머에게 있다
    # 여러 스레드가 잠금 없이 같은 객체를 수정하면 프로그램의 자료구조가 오염된다.
    # 내장 모듈 threading의 Lock클래스는 파이썬의 표준 상호 배제 잠금 구현이다.
"""
from threading import Thread, Lock


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset
        #value = getattr(counter, 'count')
        #result = value + offset
        #setattr(counter, 'count', result)

def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        # 센서 읽어옴
        # ...
        counter.increment(1)


def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

how_many = 10**5
counter = Counter()
run_threads(worker, how_many, counter)
# Counter should be 500000, found 399257
print('Counter should be %d, found %d' % (5 * how_many, counter.count))

# 스레드 A에서 실행함
value_a = getattr(counter, 'count')
# 스레드 B로 컨텍스트를 전환함
value_b = getattr(counter, 'count')
result_b = value_b + 1
setattr(counter, 'count', result_b)
# 스레드 A로 컨텍스트를 되돌림 ... 이 과정에서 이전 B Count의 증가하는 작업을 모두 없애버림
result_a = value_a
setattr(counter, 'count', result_a)

class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

counter = LockingCounter()
run_threads(worker, how_many, counter)
# Counter should be 500000, found 500000
print('Counter should be %d, found %d' % (5 * how_many, counter.count))