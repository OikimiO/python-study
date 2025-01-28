"""
    # 객체의 속성을 지연방식으로 로드하고 저장하려면 __getattr__과 __setter__을 사용하자
    # __getattr__은 존재하지 않은 속성에 접근할 때 한 번만 호출되는 반면에 __getattribute__는 속성에
      접근할 때 마다 호출된다는 점을 이해하자
    # __getattribute__와 __setattr__에서 인스턴스 속성에 직접 접근할 때 super()(즉, object클래스)
      의 메서드를 사용하여 무힌재귀가 일어나지 않게 하자

"""

class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

data = LazyDB()
# Before:  {'exists': 5}
# After:  Value for foo
# After:  {'exists': 5, 'foo': 'Value for foo'}
print('Before: ', data.__dict__)
print('After: ', data.foo)
print('After: ', data.__dict__)

class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

data = LoggingLazyDB()
# exists:  5
print('exists: ', data.exists)
# Called __getattr__(foo)
# foo:  Value for foo
# foo  Value for foo
print('foo: ', data.foo)
print('foo ', data.foo)

class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

data = ValidatingDB()
# exists:  5
print('exists: ', data.exists)
# Called __getattribute__(foo)
# foo:  Value for foo
print('foo: ', data.foo)
# Called __getattribute__(foo)
# foo:  Value for foo
print('foo: ', data.foo)