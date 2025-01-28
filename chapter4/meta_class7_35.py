"""
    # 메타클래스를 이용하면 클래스가 완전히 정의되기 전에 클래스 속성을 수정할 수 있다.
    # 디스크립터와 메타클래스는 선언적 동작과 런타임 내부 조사용으로 강력한 조합을 이룬다.
    # 메타클래스와 디스크립터를 연계하여 사용하면 메모리 누수와 weakref 모듈을 모두 피할 수 있다.
"""

class Field(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class Customer(object):
    # 클래스 속성
    first_name = Field('first_name')
    second_name = Field('second_name')
    prefix = Field('prefix')
    suffix = Field('suffix')

foo = Customer()
# Before:  '' {}
print('Before: ', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euclid'
# After:  'Euclid' {'_first_name': 'Euclid'}
print('After: ', repr(foo.first_name), foo.__dict__)

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

class DatabaseRow(object, metaclass=Meta):
    pass

class Field(object):
    def __init__(self):
        # 메타클래스가 이 속성들을 할당함
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class BetterCustomer(DatabaseRow):
    first_name = Field()
    second_name = Field()
    prefix = Field()
    suffix = Field()

foo = BetterCustomer()
# Before:  '' {}
print('Before: ', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euler'
# After:  'Euler' {'_first_name': 'Euler'}
print('After: ', repr(foo.first_name), foo.__dict__)