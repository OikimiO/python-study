# 기본 인수는 모듈 로드 시점에 함수 정의 과정에서 딱 한번만 평가된다.
# 그래서, ({}나 []와 같은) 동적 값에는 이상하게 동작하는 원인이 되기도 한다.
# 값이 동적인 키워드 인수에는 기본값으로 None을 사용하자.
# 그러고 나서 함수의 docstring에 실제 기본 동작을 문서화하자

import json
from datetime import datetime
from time import sleep

def log(message, when=datetime.now()):
    print('%s: %s' % (when, message))

# 2025-01-14 20:57:05.745773: Hi there!
log('Hi there!')
sleep(0.1)
# 2025-01-14 20:57:05.745773: Hi again!
log('Hi again!')

def log(message, when=None):
    """ Log a message with a timestamp


    Args:
        message: Message to print.
        when: datetime of when the message occured.
              Default to the present time.
    """
    when = datetime.now() if when is None else when
    print('%s: %s' % (when, message))

# 2025-01-14 21:02:36.340324: Hi there!
log('Hi there!')
sleep(0.1)
# 2025-01-14 21:02:36.445347: Hi again!
log('Hi again!')

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
# Foo: {'stuff': 5, 'meep': 1}
print('Foo:', foo)
# Bar: {'stuff': 5, 'meep': 1}
print('Bar:', bar)

# 같은 내용을 출력하는 것은 foo와 bar은 같은 딕셔너리 객체라
# 같은 값이 출력됨
assert foo is bar

def decode(data, default=None):
    """ Log a message with a timestamp

    Args:
        message: Message to print.
        when: datetime of when the message occured.
              Default to the present time.
    """
    if default is None:
        default = {}
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
# Foo: {'stuff': 5}
print('Foo:', foo)
# Bar: {'meep': 1}
print('Bar:', bar)