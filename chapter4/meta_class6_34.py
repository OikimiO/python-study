"""
    # 클래스 등록은 모듈 방식의 파이썬 프로그램을 만들 때 유용한 패턴이다
    # 메타 클래스를 이용하면 프로그램에서 기반 클래스로 서브 클래스를 만들 때 마다 자동으로
      등록 클래스를 실핼할 수 있다.
    # 메타클래스를 이용해 클래스를 등록하면 등록 호출을 절대 빠뜨리지 않으므로 오류를 방지할 수 있다.

"""

import json

class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})

class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D (%d, %d)' % (self.x, self.y)

point = Point2D(5, 3)
# Object:  Point2D (5, 3)
# Serializable:  {"args": [5, 3]}
print('Object: ', point)
print('Serializable: ', point.serialize())

class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'BetterPoint2D (%d, %d)' % (self.x, self.y)

point = BetterPoint2D(5, 3)
# Before:  BetterPoint2D (5, 3)
print('Before: ', point)
data = point.serialize()
# After:  {"args": [5, 3]}
print('After: ', data)
after = BetterPoint2D(5, 3).deserialize(data)
# After:  BetterPoint2D (5, 3)
print('After: ', after)

class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args
        })

registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class EventBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(self, x, y)
        self.x = x
        self.y = y

#register_class(EventBetterPoint2D)

# 에러 발생하는데 이유를 모르겠넹;;
#point = EventBetterPoint2D(5, 3)
#print('Before: ', point)
#data = point.serialize()
#print('Serialized: ', data)
#after = deserialize(data)
#print('After: ', after)

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass

class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

v3 = Vector3D(10, -7, 3)
print('Before: ', v3)
data = v3.serialize()
# Serialized:  {"class": "Vector3D", "args": [10, -7, 3]}
print('Serialized: ', data)
print('After: ', deserialize(data))
