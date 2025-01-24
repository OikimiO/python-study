"""
    # 직접 디스크립터 클래스를 정의하여 @property메서드의 동작과 검증을 재사용하자
    # WeakKeyDictionary를 사용하여 디스크립터 클래스가 메모리 누수를 일으키지 않게 하자.
    # __getattribute__가 디스크립터 프로토콜을 사용하여 속성을 얻어오고 설정하는 원리를 정확히
      이해하려는 함정에 빠지지 말자
"""

from weakref import WeakKeyDictionary

class Homework(object):
    def __init__(self):
        self.grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not(0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value

galileo = Homework()
galileo.grade = 95

class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value


class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
# First  82 is right
print('First ', first_exam.writing_grade, 'is right')
# Second  75 is right
print('Second ', second_exam.writing_grade, 'is right')