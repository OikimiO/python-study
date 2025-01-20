"""
    # 쓰임새가 간단할 때는 list나 dict 같은 파이썬의 컨테이너 타입에서 직접 상속받게 하자
    # 커스텀 컨테이너 타입을 올바르게 구현하는데 필요한 많은 메서드에 주의해야 한다.
    # 커스텀 컨테이너 타입이 collections.abc에 정의된 인터페이스에서 상속받게 만들어서
      클래스가 필요한 인터페이스, 동작과 일치하게 하자
"""

class FreequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts

foo = FreequencyList(['a','b','a','c','b','a','d'])
# Length is 7
print('Length is', len(foo))
foo.pop()
# After pop ['a', 'b', 'a', 'c', 'b', 'a']
print('After pop', repr(foo))
# Frequency {'a': 3, 'b': 2, 'c': 1}
print('Frequency', foo.frequency())

class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left  = left
        self.right = right

bar = [1,2,3]
assert bar[0] == bar.__getitem__(0)

class IndexableNode(BinaryNode):
    def _search(self, count, index):
        return 0

    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError('Index Out of Range')
        return found.value