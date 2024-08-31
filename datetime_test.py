import datetime
from datetime import timezone

d = datetime.date.today()
t = datetime.datetime.min.time()
t_max = datetime.datetime.max.time()

cur_time = datetime.datetime.combine(d, t, tzinfo=timezone.utc)
ts = int(cur_time.timestamp())

currentdate = datetime.datetime.today()
timestamp_start_day = int(
    currentdate.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0).timestamp())

print(t_max)
print(timestamp_start_day)
