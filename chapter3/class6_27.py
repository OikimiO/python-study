"""
 # 파이썬 컴파일러는 비공개 속성을 엄격하게 강요하지 않는다.
 # 서브클래스가 내부 API와 속성에 접근하지 못하게 막기보다는 처음부터 내부 API와 속성으로
   더 많은 일을 할 수 있게 설계하자
 # 비공개 속성에 대한 접근을 강제로 제어하지 말고 보호 필드를 문서화해서 서브 클래스에
   필요한 지침을 제공하자
 # 직접 제어할 수 없는 서브클래스와 이름이 충돌하지 않게 할 때만 비공개 속성을 사용하는 방안을 고려하자
"""
class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field

foo = MyObject()

assert foo.public_field == 5

class MyOtherObject(object):
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71

class MyParentObject(object):
    def __init__(self):
        self.__private_field = 71

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field

baz = MyChildObject()
# AttributeError: 'MyChildObject' object has no attribute '_MyChildObject__private_field'. Did you mean: '_MyParentObject__private_field'?
#baz.get_private_field()

assert baz._MyParentObject__private_field == 71
# {'_MyParentObject__private_field': 71}
print(baz.__dict__)

class MyClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

foo = MyClass(5)

# AssertionError
#assert foo.get_value() == 5

class MyIntegerSubClass(MyClass):
    def get_value(self):
        return int(self.MyClass__value)

foo = MyIntegerSubClass(5)
# AttributeError: 'MyIntegerSubClass' object has no attribute 'MyClass__value'. Did you mean: '_MyClass__value'?
# assert foo.get_value() == 5

class MyClass(object):
    def __init__(self, value):
        self._value = value

class ApiClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'

a = Child()
# hello and hello should be different
print(a.get(), 'and' , a._value, 'should be different')

class ApiClass(object):
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'

a = Child()
# 5 and hello should be different
print(a.get(), 'and' , a._value, 'should be different')