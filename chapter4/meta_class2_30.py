"""
    # 간단한 공개 속성을 사용하여 새 클래스 인터페이스를 정의하고 세터와 게터 메서드는 사용하지 말자
    # 객체의 속성에 접근할 때 특별한 동작을 정의하려면 @property를 사용하자
    # @property 메서드에서 최소 놀람 규칙을 따르고 이상한 부작용은 피하자
    # @property 메서드가 빠르게 동작하도록 만들자. 느리거나 복잡한 작업은 일반 메서드로 하자
"""
from datetime import datetime, timedelta

class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota

def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True

bucket = Bucket(60)
fill(bucket, 100)
# Bucket(quota=100)
print(bucket)

# Had 99 quota
if deduct(bucket,99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

# Bucket(quota=1)
print(bucket)

#Not enough for 3 quota
if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')

# Bucket(quota=1)
print(bucket)

class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return ('Bucket(max_quota=%d, quota_consumed=%d)') % (self.max_quota, self.quota_consumed)