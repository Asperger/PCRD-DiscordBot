timer_usage = 0
timer_member_list = {}

from datetime import datetime
from pytz import timezone    
eu_moscow = timezone('Europe/Moscow')

def get_settlement_time_object():
    return datetime.now(eu_moscow)

def get_settlement_time():
    return datetime.now(eu_moscow).strftime('%Y-%m-%d')