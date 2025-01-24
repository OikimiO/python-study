"""
    # 기존 인스턴스 속성에 새 기능을 부여하려면 @property를 사용하자
    # @property를 사용하여 점점 나은 데이터 모델로 발전시키자
    # @property를 너무 많이 사용한다면 클래스와 이를 호출하는 모든 곳을 리팩토링하는 방안을 고려하자
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

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # 새 기간의 할당량을 리셋함
            self.quota_consumed = 0
            self.max_quota = 0
        if delta < 0:
            # 새 기간의 할당량을 채움
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # 기간 동안 할당량을 소비함
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

bucket = Bucket(60)
# Initial Bucket(max_quota=0, quota_consumed=0)
print('Initial', bucket)
fill(bucket, 100)
# filled Bucket(max_quota=100, quota_consumed=0)
print('filled', bucket)

if deduct(bucket, 99):
    # Had 99 quota
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

# Now Bucket(max_quota=100, quota_consumed=99)
print('Now', bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    # Not enough for 3 quota
    print('Not enough for 3 quota')

# Still Bucket(max_quota=100, quota_consumed=99)
print('Still', bucket)