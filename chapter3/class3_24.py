# 파이썬에서는 클래스별로 생성자를 한 개(__init__)만 만들 수 있다. 
# 클래스에 필요한 다른 생성자를 정의하려면 @classmehtod를 사용하자
# 구체 서브클래스들을 만들고 연결하는 범용적인 방법을 제공하려면 클래스 메서드 다형성을 이용하자

from tempfile import TemporaryDirectory
import os
from threading import Thread

# 글루 코드(Glue Code): 다양한 시스템, 모듈, 또는 컴포넌트를 연결하는 역할을 하는 코드

# 맵 리듀스: 대규모 데이터 처리를 위한 프로그래밍 모델이자 그 모델을 구현한 알고리즘
#           이 방식은 데이터를 분산 환경에서 효율적으로 처리하고 분석할 수 있도록 돕습니다
# Map 단계: 주로 키-값 쌍의 형태로 데이터를 처리
# Reduce 단계: Map 단계에서 처리된 결과를 모아서 최종적인 출력

class InputData(object):
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path
        
    # read: 클래스에서 처리할 바이트 데이터를 반환하는 표준 인터페이스
    def read(self):
        return open(self.path).read()

class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None
        
    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError
    
class LineCounterWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result
# 글루 코드
""" 
    data_dir에서 파일들을 읽고, 각 파일에 대해 PathInputData 객체를 생성하는 역할
    :param data_dir: 저장할 폴더
"""
def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


# 글루 코드
"""
   입력 데이터를 받아서 각 데이터를 처리할 수 있는 LineCounterWorker 객체들을 생성
   :param input_list: 입력받은 리스트
"""
def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCounterWorker(input_data))
    return workers

# 글루 코드
"""
   작업자들을 실행하고, 그 결과를 하나로 합치는 과정
   :param workers: 작업자들
"""
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    
    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result

# 글루 코드
"""
   전체 데이터를 처리하는 흐름을 관리
   :param data_dir: 저장할 폴더
"""
def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

# 글루 코드
""" 
    테스트 파일을 tmpdir에 작성하는 역할
    :param tmpdir: 저장할 임시 폴더
"""
def write_test_files(tmpdir):
    filenames = ['file1.txt', 'file2.txt', 'file3.txt']
    lines = [
        "This is the first file.\nIt has two lines.\n",  # file1.txt
        "Second file here.\nIt also has two lines.\n",  # file2.txt
        "And this is the third file.\nIt has three lines.\nOne more line.\n"  # file3.txt
    ]
    
    for filename, content in zip(filenames, lines):
        file_path = os.path.join(tmpdir, filename)
        with open(file_path, 'w') as f:
            f.write(content)



with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    result = mapreduce(tmpdir)
    
print('There are', result, 'lines')


class GenericInputData(object):
    def read(self):
        raise NotImplementedError
    
    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError

class PathInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path
        
    # read: 클래스에서 처리할 바이트 데이터를 반환하는 표준 인터페이스
    def read(self):
        return open(self.path).read()
    
    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir,name))

class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None
        
    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError
    
    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

class LineCounterWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result

def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {'data_dir': tmpdir}
    result = mapreduce(LineCounterWorker, PathInputData, config)