from datetime import datetime,timedelta

def to_datetime(text):
    return datetime.strptime(text,'%Y-%m-%dT%H:%M:%S.%fZ')

def corrected_datetime(text):
    return to_datetime(text)+timedelta(hours=7)

def daily_log_dates():
    return '"'+datetime.strftime(datetime.utcnow(),"%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z"',\
           '"'+datetime.strftime(datetime.utcnow()-timedelta(hours=24),"%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z"'
