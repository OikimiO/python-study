# def문에서 *args를 사용하면 함수에서 가변 개수의 위치 인수를 받을 수 있다.
# * 연산자를 쓰면 시퀀스에 들어 있는 아이템을 함수의 위치 인수로 사용할 수 있다.
# 제너레이터와 * 연산자를 함께 사용하면 프로그램 메모리 부족으로 망가질 수도 있다.
# *args를 받는 함수에 새 위치 파라미터를 추가하면 정말 찾기 어려운 버그가 생길 수도 있다.

def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print("%s: %s" % (message, values_str))

# My numbers are: 1, 2
log('My numbers are', [1,2])

# Hi there
log('Hi there', [])

def log(message, *values):
    if not values:
        print(message)
    else:
        value_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, value_str))
# My numbers are: 1, 2
log('My numbers are', 1, 2)

# Hi there
log('Hi there')

favorites = [7, 33, 99]
# favorite colors: 7, 33, 99
log('favorite colors', *favorites)

def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

# (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
it = my_generator()
my_func(*it)

def log(sequence, message, *values):
    if not values:
        print("%s: %s" % (sequence, message))
    else:
        value_str = ', '.join(str(x) for x in values)
        print("%s: %s %s" % (sequence, message, value_str))

# 1: Favorites 7, 33
log(1, 'Favorites', 7, 33) # 새로운 용법은 OK

# Favorites number: 7 33
log('Favorites number', 7, 33) # 오래된 용법은 제대로 동작하지 않음