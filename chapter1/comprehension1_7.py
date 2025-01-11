# 간단한 연산엔 컴프리헨션이 더 나음
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
a = [1,2,3,4,5,6,7,8,9,10]
square = [x ** 2 for x in a]
print(square)

# map 사용: lambda를 사용해 깔끔해 보이지 않음
square2 = map(lambda x: x ** 2, a)
print(square2)

# 컴프리헨션: 2로 나누어 떨어지는 숫자의 제곱만 계산
# [4, 16, 36, 64, 100]
event_squares = [x ** 2 for x in a if x % 2 == 0]
print(event_squares)

# 컴프리헨션: 2로 나누어 떨어지는 숫자의 제곱만 계산
# map 사용: 여전히 어려움..
alt = map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, a))
assert event_squares == list(alt)

# dictionary를 {rank: name}로 변경하고 name 배열의 길이를 출력
# {1: 'ghost', 2: 'habanero', 3: 'cayenne'}
# {8, 5, 7}
chile_ranks = {'ghost':1, 'habanero': 2, 'cayenne': 3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}
chile_len_set = {len(name) for name in rank_dict.values()}
print(rank_dict)
print(chile_len_set)