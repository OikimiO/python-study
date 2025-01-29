"""
    # 코루틴은 함수 수만개를 마치 동시에 실행하는 것처럼 실행하는 효과적인 방법을 제공한다.
    # 제너레이터 안에서 yield표현식의 값은 외부 코드에서 제너레이터의 send메서드에 전달한 값이다.
    # 코루틴은 프로그램의 핵심 로직을 주변 환경과 상호 작용하는 코드로부터 분리할 수 있는 강력한 도구다.
    # 파이썬 2는 yield from 문법과 제너레이터에서 값을 반환하는 기능을 지원하지 않는다.
"""
from collections import namedtuple


def my_coroutine():
    while True:
        received = yield
        print('Received:', received)

it = my_coroutine()
next(it) # 코루틴을 준비함
# Received: First
# Received: Second
it.send('First')
it.send('Second')

def minimize():
    current = yield
    while True:
        value = yield current
        current = min(value, current)

it = minimize()
next(it) # 제너레이터를 준비함
# 10
# 4
# 4
# -1
print(it.send(10))
print(it.send(4))
print(it.send(22))
print(it.send(-1))

ALIVE = '*'
EMPTY = '-'

Query = namedtuple('Query', ('y','x'))

def count_neighbors(y, x):
    n_ = yield Query(y+1, x+0) # 북쪽
    ne = yield Query(y+1, x+1) # 북동쪽
    e_ = yield Query(y+0, x+1) # 동쪽
    se = yield Query(y-1, x+1) # 남동쪽
    s_ = yield Query(y-1, x+0) # 남쪽
    sw = yield Query(y-1, x-1) # 남서쪽
    w_ = yield Query(y+0, x-1) # 서쪽
    nw = yield Query(y+1, x-1) # 북서쪽

    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state  == ALIVE:
            count += 1
    return count

it = count_neighbors(10, 5)
q1 = next(it) # 첫번째 쿼리를 받음
print('1 yield: ', q1)
q2 = it.send(ALIVE) # q1 상태를 보내고 q2를 받음
print('2 yield: ', q2)
q3 = it.send(ALIVE) # q2 상태를 보내고 q3를 받음
print('3 yield: ', q3)
q4 = it.send(ALIVE) # q3 상태를 보내고 q4를 받음
print('4 yield: ', q4)
q5 = it.send(ALIVE) # q4 상태를 보내고 q5를 받음
print('5 yield: ', q5)
q6 = it.send(ALIVE) # q5 상태를 보내고 q6를 받음
print('6 yield: ', q6)
q7 = it.send(ALIVE) # q6 상태를 보내고 q7를 받음
print('7 yield: ', q7)
q8 = it.send(ALIVE) # q7 상태를 보내고 q8를 받음
print('8 yield: ', q8)
try:
    count = it.send(EMPTY)
except StopIteration as e:
    # 원래는 count가 2인데... 난 7이 나오는구먼..
    print('Count: ', e.value)

Transition = namedtuple('Transition', ('y','x','state'))

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY # 죽음: 너무 적음
        elif neighbors > 3:
            return EMPTY # 죽음: 너무 많음
    else:
        if neighbors == 3:
            return ALIVE # 되살아남

    return state

def step_cell(y, x):
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)

it = step_cell(10, 5)
q0 = next(it) # 초기 위치 쿼리
print('Me: ', q0)
q1 = it.send(ALIVE) # 내 상태를 전달하고 이웃 쿼리를 받음
print('Q1: ', q1)
# ...


#... 이하는 다음에 진행할 것