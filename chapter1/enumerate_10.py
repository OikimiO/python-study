import random

# random.randint(start, stop): start 이상 stop 이하 범위의 정수 난수 생성
# 일반 루프: for문을 1~ 63까지 반복하면서 random.randint의 값이 1이 되는 순간의 i만큼 래프트 쉬프트한 값을 찾기
# 12718974999555530603 ... 다를 수도 있음
random_bits = 0
for i in range(64):
    if random.randint(0, 1):
        random_bits |= 1 << i

print(random_bits)

# 일반 루프: ~ is delicious를 출력
# vanilla is delicious
# chocolate is delicious
# pecan is delicious
# strawberry is delicious
flavor_list = ['vanilla','chocolate','pecan','strawberry']
for flavor in flavor_list:
    print('%s is delicious' % flavor)

# 일반 루프: 인덱스별로 아이스크림을 출력
# 출력 형식 %d: %s
# 단점: 배열의 원소를 인덱스로 접근해 읽기 불편
# 1: vanilla
# 2: chocolate
# 3: pecan
# 4: strawberry
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d: %s' % (i+1, flavor))

# enumerate: 인덱스별로 아이스크림을 출력
# 장점: 일반 루프에 비해 간결해 읽기 쉬움
# 1: vanilla
# 2: chocolate
# 3: pecan
# 4: strawberry
for i, flavor in enumerate(flavor_list):
    print('%d: %s' % (i+1, flavor))

# enumerate를 활용해 인덱스의 시작값을 1로 함
for i, flavor in enumerate(flavor_list, 1):
    print('%d: %s' % (i, flavor))