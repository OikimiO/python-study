from urllib.parse import parse_qs

# dictionary: key-value로 구성된 자료구조
# parse_qs: 파라미터 쿼리를 배열로 뽑는 함수
# keep_blank_values=True: 파라미터 쿼리 중 빈갑을 포함해 키 값을 출력한다.
my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)

# dictionary인 my_values를 str 타입으로 리턴
# <class 'str'>
print(type(repr(my_values)))

# str 타입인 value를 출력
# {'red': ['5'], 'blue': ['0'], 'green': ['']}
print(repr(my_values))

# my_values를 dictionary 타입으로 리턴
# <class 'dict'>
print(type(my_values))

# value 출력
# {'red': ['5'], 'blue': ['0'], 'green': ['']}
print(my_values)

# ['5']
print(repr(my_values.get("red")))

# ['0']
print(my_values.get("blue"))

# None
print(my_values.get("opacity"))


# my_values 키값인 red가 빈값이 아닌 경우 첫번쨰 인덱스의 값을 반환하고 그렇지 않을 경우 0을 반환
# red는 ['5']라는 값이 존재하기에 true를 리턴하여 0번쨰 인덱스[0]의 값을 리턴
# 5
print(my_values.get("red",[''])[0] or 0)


# my_values 키값인 green가 빈값이 아닌 경우 첫번쨰 인덱스의 값을 반환하고 그렇지 않을 경우 0을 반환
# green은 빈값('')임으로 false로 인식 되어 0을 리턴
# 0
print(my_values.get("green",[''])[0] or 0)


# my_values 키값인 opacity가 빈값이 아닌 경우 첫번쨰 인덱스의 값을 반환하고 그렇지 않을 경우 0을 반환
# opacity는 my_values에 존재하지 않으므로, 처음부터 false로 인식되어 0을 리턴
# 0
print(my_values.get("opacity",[''])[0] or 0)

# my_values key값 중 red를 int로 변환
# 단점: 데이터 처리과정이 너무 복잡함
# 5
print(int(my_values.get('red',['0'])[0] or 0))


# 단점 해결: if/else를 사용
green = my_values.get("green",['0'])
if green[0]:
    print(int(green[0]))
else:
    print(0)

# 부가 사항: 재 사용을 한다면? 함수 사용
def convert_to_int(values, key, default = 0):
    data = values.get(key, [''])
    if data[0]:
        return int(data[0])
    else:
        return default

# 5
green = convert_to_int(my_values, 'green')
print(green)

# 0
red = convert_to_int(my_values, 'red')
print(red)