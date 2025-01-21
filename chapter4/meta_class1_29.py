"""
    # 간단한 공개 속성을 사용하여 새 클래스 인터페이스를 정의하고 세터와 게터 메서드는 사용하지 말자
    # 객체의 속성에 접근할 때 특별한 동작을 정의하려면 @property를 사용하자
    # @property 메서드에서 최소 놀람 규칙을 따르고 이상한 부작용은 피하자
    # @property 메서드가 빠르게 동작하도록 만들자. 느리거나 복잡한 작업은 일반 메서드로 하자
"""

class OldResistor(object):
    def __init__(self, ohms):
       self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

r0 = OldResistor(50e3)
# Before: 50000.0
print('Before: %5r' % r0.get_ohms())
r0.set_ohms(10e3)
# After: 10000.0
print('After: %5r' % r0.get_ohms())

class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3
r1.ohms += 5e3

class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

r2 = VoltageResistance(1e3)
# Before:     0 amps
print('Before: %5r amps' % r2.current)
r2.voltage = 10
# After:  0.01 amps
print('After: %5r amps' % r2.current)

class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

# r3 = BoundedResistance(1e3)
# ValueError: 0.000000 ohms must be > 0
# r3.ohms = 0
# ValueError: -5.000000 ohms must be > 0
# r3 = BoundedResistance(-5)

class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError('Can`t set attribute')
        self._ohms = ohms

r4 = FixedResistance(1e3)
# AttributeError: Can`t set attribute
# r4.ohms = 2e3

class MysteriousResistor(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError('Can`t set attribute')
        self._ohms = ohms

r7 = MysteriousResistor(10)
r7.current = 0.01
# Before:     0 amps
print('Before: %5r amps' % r7.voltage)
# 잘못된 방식
r7.ohms
# After:  0.01 amps
print('After: %5r amps' % r7.voltage)