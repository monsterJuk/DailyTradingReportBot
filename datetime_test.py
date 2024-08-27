import datetime

currentdate = datetime.datetime.today()
timestamp_start_cur_day = int(currentdate.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()) * 1000
timestamp_end_cur_day = int(currentdate.replace(hour=23, minute=59, second=59, microsecond=999999).timestamp()) * 1000
timestamp_start_prev_day = timestamp_start_cur_day - 86400000
timestamp_end_prev_day = timestamp_end_cur_day - 86400000





print(timestamp_end_cur_day)
