"""
    # 파이프라인은 여러 파이썬 스레드를 사용하여 동시에 실행하는 작업의 순서를 구성하기에 아주 좋은 방법이다
    # 병행 파이프라인을 구축할 때는 많은 문제(바쁜 대기, 작업자 중단, 메모리 부족)가 일어날 수 있다는 점을 주의하자
    # Queue 클래스는 연산 블로킹, 버퍼 크기, 조인 등 견고한 파이프라인을 만드는데 필요한 기능을 모두 갖췄다.
"""
import time
from _ctypes import resize
from collections import deque
from distutils.command import upload
from queue import Queue
from threading import Lock, Thread

from pip._internal.network import download


class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def fun(self):
        while True:
            self.polled_count += 1
        try:
            item = self.in_queue.get()
        except IndexError:
            sleep(0.01) # 처리할 아이템이 없음
        else:
            result = self.func(item)
            self.out_queue.put(result)
            self.work_done += 1

download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue)
]

for thread in threads:
    thread.start()
for _ in range(1000):
    download_queue.put(object())

# 너무 느려서 종료시킴
#while len(done_queue.items) < 1000:
    # 기다리는 동안 유용한 작업을 진행
#    a = 1

#processed = len(done_queue.items)
#polled = sum(t.polled_count for t in threads)
#print('Processed', processed, 'items after polling', polled, 'items')

queue = Queue()
def consumer():
    print('Consumer waiting')
    queue.get()
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()
# Consumer waiting
# Producer putting
#
# Consumer done
# Producer done
print('Producer putting')
queue.put(object())
thread.join()
print('Producer done')

queue = Queue(1) # 크기가 1인 버퍼
def consumer():
    time.sleep(0.1) # 대기
    queue.get() # 두 번째로 실행함
    print('Consumer got 1')
    queue.get() # 네번째로 실행함
    print('Consumer got 2')

thread = Thread(target=consumer)
thread.start()

# Producer put 1
# Consumer got 1
# Producer put 2
# Consumer got 2
# Producer done
queue.put(object())
print('Producer put 1') # 첫 번째로 실행함
queue.put(object())
print('Producer put 2') # 두 번째로 실행함
thread.join()
print('Producer done')

in_queue = Queue()

def consumer():
    print('Consumer waiting')
    work = in_queue.get() # 두 번째로 완료함
    print('Consumer working')
    # 작업을 수행함
    # ...
    print('Consumer done')
    in_queue.task_done() # 세 번째로 완료함

Thread(target=consumer).start()

# Consumer waiting
# Producer waiting
# Consumer working
# Consumer done
# Producer done
in_queue.put(object()) # 첫 번째로 완료함
print('Producer waiting')
in_queue.join() # 네 번째로 완료함
print('Producer done')

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return # 스레드가 종료되게 함
                yield item
            finally:
                self.task_done()

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue)
]

for thread in threads:
    thread.start()
for _ in range(1000):
    download_queue.put(object())

# 오류가 나는데 왜 나는 지는 모르겠당..
download_queue.close()
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'items finished')