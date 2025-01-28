"""
    # 자식 프로세스를 실행하고 자식 프로세스의 입출력 스트림을 관리하려면 subprocess모듈을 사용하자
    # 자식 프로세스는 파이썬 인터프리터에서 병렬로 실행되어 CPU 사용을 극대화하게 해준다.
    # communicate에 timeout 파라미터를 사용하여 자식 프로세스들이 교착 상태(deadlock)에 빠지거나
      멈추는 상황을 막자
"""

import os
import subprocess
from time import time

proc = subprocess.Popen(
    ['echo', 'Hello from the child'],
    stdout= subprocess.PIPE
)
out, err = proc.communicate()
# Hello from the child
print(out.decode('utf-8'))

proc = subprocess.Popen(['sleep', '0.3'])
# Working...
# Working...
# Exit status 0
#while proc.poll() is None:
#    print('Working...')

#print('Exit status', proc.poll())

def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)

for proc in procs:
    proc.communicate()
end = time()
# Finished in 0.110 seconds
print('Finished in %.3f seconds' % (end - start))

def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    proc.stdin.write(data)
    proc.stdin.flush() # 자식 프로세스가 입력을 반드시 받게 함
    return proc

#procs = []
#for _ in range(3):
#    data = os.urandom(10)
#    proc = run_openssl(data)
#    procs.append(proc)

#for _ in procs:
#    out, err = proc.communicate()
#    print(out[-10:])

def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5'],
        stdin=input_stdin,
        stdout=subprocess.PIPE
    )
    return proc

input_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    input_procs.append(proc)
    hash_procs = run_md5(proc.stdout)
#     hash_procs.append(hash_procs)

# 오류 남.. 원인은 모르겠음..
#for proc in input_procs:
#    proc.communicate()

#for proc in hash_procs:
#    out, err = proc.communicate()
#    print(out.strip())

proc = run_sleep(10)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

# Exit status -15
print('Exit status', proc.poll())
