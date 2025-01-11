# 일반 루프: Loop %d를 출력(%d는 0~2, else는 Else block!을 출력)
# 단점: 아래와 같은 코드는 사용자들로 하여 오해를 일으킴
# Loop 0
# Loop 1
# Loop 2
# Else block!
for i in range(3):
    print('Loop %d' % i)
else:
    print('Else block!')

# 다음의 예제처럼 사용하면 다른 코드를 사용하는 이들이 이해하기가 어려움
# 입력하는 두숫자가 서로소인지 찾는 코드
a=4
b=9
for i in range(2, min(a,b)+1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')

# 두 숫자가 서로소 인지 찾는 함수
# 그래서, 함수로 만들어 유지보수에 편하게 사용
# a=4, b=9 두수는 서로소입니다.
def coprime(a,b):
    for i in range(2, min(a,b)+1):
        if a % i == 0 and b % i == 0:
            return False
    return True

if coprime(4,9):
    print('두수는 서로소입니다.')
else:
    print('두수는 서로소가 아닙니다.')