"""
    # 서브 클래스 타입의 객체를 생성하기에 앞서 서브클래스가 정의 시점부터 제대로 구성되었음을 보장하려면
      메타클래스를 사용하자
    # 파이썬 2와 파이썬 3의 메타클래스 문법은 약간 다르다.
    # 메타클래스의 __new__메서드는 class문의 본문 전체가 처리된 후에 실행된다
"""


# (
#  <class '__main__.Meta'>,
#  'MyClass',
#  (<class 'object'>,),
#  {'__module__': '__main__',
#   '__qualname__': 'MyClass',
#   'stuff': 123,
#   'foo': <function MyClass.foo at 0x100fa09d0>
#   }
# )
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print((meta, name, bases, class_dict))
        return type.__new__(meta, name, bases, class_dict)

class MyClass(object, metaclass=Meta):
    stuff = 123

    def foo(self):
        pass

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # 추상 Polygon 클래스는 검증하지 않음
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygones need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(object, metaclass=ValidatePolygon):
    sides = None # 서브클래스에서 설정함

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

# Before class
print('Before class')
class Line(Polygon):
    # Before class
    print('Before sides')
    # ValueError: Polygones need 3+ sides
    sides = 1
    print('After sides')
# After sides
print('After class')