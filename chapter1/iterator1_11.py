# 컴프리헨션: 배열의 문자 길이만큼 출력
# [7, 4, 5]
names = ['Cecilla','Lise','Marie']
letters = [len(n) for n in names]
print(letters)

# 일반 루프: 문자열 중 가장 긴 문자를 출력
# 단점: i인 인덱스를 중복(letters[i], names[i])해서 사용하기에 읽기가 불편
# Cecilla
longest_name = None
max_letters = 0

for i in range(len(names)):
    count = letters[i]
    if count > max_letters:
        longest_name = names[i]
        max_letters = count

print(longest_name)

# enumerate: 문자열 중 가장 긴 문자를 출력
# Cecilla
for i, name in enumerate(names):
    count = letters[i]
    if count > max_letters:
        longest_name = name
        max_letters = count

print(longest_name)

# zip: 문자열 중 가장 긴 문자를 출력
# zip을 사용하면 enumerate보다 더 간결해짐
# Cecilla
for name, count in zip(names, letters):
    if count > max_letters:
        longest_name = name
        max_letters = count

print(longest_name)

# zip사용의 문제점
# 1. zip은 생성한 모든 튜플은 반환하기에 메모리에 부담이 됨
# 2. 입력 데이터들의 길이가 다르면 짧은 것을 길이를 기준으로 프린트함
#  - names에 Rosalind를 넣어도 출력이 되지 않음
# Cecilla
# Lise
# Marie
names.append('Rosalind')
for name, count in zip(names, letters):
    print(name)