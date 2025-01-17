# 다른 딕셔너리나 긴 튜플을 값으로 담은 딕셔너리를 생성하지 말자.
# 정식 클래스의 유연성이 필요 없다면 가벼운 불변 데이터 컨테이너에는 namedtuple을 사용하자
# 내부 상태를 관리하는 딕셔너리가 복잡해지면 여러 헬퍼 클래스를 사용하는 방식으로 관리 코드를 바꾸자

import collections

class SimpleGradebook(object):
    def __init__(self):
        self._grades = {}
    
    def add_student(self, name):
        self._grades[name] = []
    
    def report_grade(self, name, score):
        self._grades[name].append(score)
    
    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

book = SimpleGradebook()
book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 90)

# 90.0
print(book.average_grade('Isaac Newton'))

class BySubjectGradeboot(object):
    def __init__(self):
        self._grades = {}
    
    def add_student(self, name):
        self._grades[name] = {}
        
    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        #print(by_subject)
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)
        
    def average_grade(self, name):
        #print(self._grades)
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            #print(grades)
            #print(len(grades))
            total += sum(grades)
            count += len(grades)
        return total/count

book = BySubjectGradeboot()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75)
book.report_grade('Albert Einstein', 'Math', 65)
book.report_grade('Albert Einstein', 'Gym', 90)
book.report_grade('Albert Einstein', 'Gym', 95)

# 81.25
print(book.average_grade('Albert Einstein'))

# 클래스 사용법이 어려워짐
class WeightGradebook(object):
    def __init__(self):
        self._grades = {}
    
    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append((score, weight))
        #print(by_subject)
        
    def average_grade(self, name):
        #print('average_grade')
        by_subject = self._grades[name]
        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            #print(subject)
            #print(scores)
            subject_avg, total_weight = 0, 0
            for score, weight in scores:
                subject_avg += score
                total_weight += weight
            
            subject_avg = (subject_avg + (subject_avg * total_weight)) / len(scores)
            #print(subject_avg)
            #print(total_weight)
            #print(len(scores))
            score_sum += subject_avg
            score_count += 1
        
        return score_sum / score_count
    
book = WeightGradebook()
book.add_student('Albert Einstein')
# 단점: 전달하는 파라미터의 길이가 길어질 수록 인수에 들어있는 내용이 무엇을 말하는지 알기 어려움
book.report_grade('Albert Einstein', 'Math', 75, 0.10)
book.report_grade('Albert Einstein', 'Math', 65, 0.10)
book.report_grade('Albert Einstein', 'Gym', 90, 0.10)
book.report_grade('Albert Einstein', 'Gym', 95, 0.10)
# 97.5
print(book.average_grade('Albert Einstein'))

# namedtuple를 이용하면 작은 불변 데이터 클래스를 쉽게 정의할 수 있음
# namedtuple의 제약
#  1. namedtuple로 만들 클래스에 기본 인수 값을 설정할 수 없다. 
#     그래서 데이터에 선택적인 속성이 많으면 다루기 힘들어진다.
#     속성을 사용할 때는 클래스를 직접 정의하는게 나을 수 있다.
#  2. namedtuple 인스턴스의 속성 값을 여전히 숫자로 된 인덱스와 순회 방법으로
#     접근 가능하다.
#     특히 외부 API로 노출한 경우에는 의도와 다르게 사용되어 나중에 실제 클래스로
#     바꾸기 더 어려울 수 있다. 
#     
Grade = collections.namedtuple('Grade', ('score','weight'))

class Subject(object):
    def __init__(self):
        self._grades = []
    
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
    
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

class Student(object):
    def __init__(self):
        self._subjects = {}
    
    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]
    
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

class Gradebook(object):
    def __init__(self):
        self._students = {}
    
    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]
    
book = Gradebook()
albert = book.student('Albert Einstein')
math = albert.subject('Math')
math.report_grade(80, 0.10)
math.report_grade(75, 0.10)
gym = albert.subject('Gym')
gym.report_grade(90, 0.10)
gym.report_grade(95, 0.10)

#85.0
print(albert.average_grade())
