from datetime import datetime
from pytz import timezone

timer_usage = 0
timer_member = 0
timer_channel = 0

_eu_moscow = timezone('Europe/Moscow')

def get_settlement_time_object():
    return datetime.now(_eu_moscow)

def get_settlement_time():
    return datetime.now(_eu_moscow).strftime('%Y-%m-%d')