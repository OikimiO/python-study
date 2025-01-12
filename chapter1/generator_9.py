# 컴플리헨션은 입력이 적을 떄는 괜찮지만 클 때는 메모리 소모가 높음
# 특히 네트워크 소켓 사용시 문제가 발생할 수 있음
# 그래서, 제너레이터를 활용해 배열의 원소를 하나씩 확인

# 컴프리헨션: 문자열의 길이를 배열로 출력
# [100, 57]
value = [len(x) for x in open("../tmp/my_file.txt")]
print(value)

# 제너레이터: 문자열의 길이를 하나씩 출력
# 100
# 57
it = (len(x) for x in open("../tmp/my_file.txt"))
print(next(it))
print(next(it))

# 제너레이터: 문자열의 길이를 0.5 제곱
# (100, 10.0)
# (57, 7.54983443527075)
it = (len(x) for x in open("../tmp/my_file.txt"))
roots = ((x, x**0.5) for x in it)
print(next(roots))
print(next(roots))