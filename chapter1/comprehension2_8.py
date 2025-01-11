matrix = [[1,2,3],[4,5,6],[7,8,9]]
# 컴프리헨션: 2차원 배열을 1차원 배열로 변환
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
flat = [x for row in matrix for x in row]
print(flat)

# 2차원 배열의 원소를 제곱으로 변환
# [[1, 4, 9], [16, 25, 36], [49, 64, 81]]
square = [[x ** 2 for x in row] for row in matrix]
print(square)

# 컴프리헨션: 3차원 배열을 1차원 배열로 변환
# 단점: 여러 줄로 구분해야 함
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
my_lists = [
    [[1,2,3],[4,5,6]],
    [[7,8,9],[10,11,12]]
]
flat = [
        x for sublist1 in my_lists
          for sublist2 in sublist1
          for x in sublist2
        ]
print(flat)

# 일반 루프문: 3차원 배열을 1차원 배열로 변환
# 컴프리헨션으로 구현된 것보단 이해하기가 쉬어짐
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
            flat.extend(sublist2)

print(flat)

# 4보다 크면서 짝수인 원소를 배열로 뽑기
# [6, 8, 10]
# [6, 8, 10]
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]

print(b)
print(c)

# 이차원 배열에 속한 배열의 합이 10 이상이면서 해당 배열의 원소가 3으로 나누어 떨어지는 수
# 단점: 코드가 난해져서 유지 보수가 어려움, 다음의 방법은 사용 하지 말것
# [[6], [9]]
filtered = [
            [x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10
            ]
print(filtered)