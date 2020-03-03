from datetime import datetime
from pytz import timezone

import schedule
import time
import threading
from utils.line_manager import clear_line

timer_usage = 0
timer_member = 0
timer_channel = 0

_eu_moscow = timezone('Europe/Moscow')

def get_settlement_time_object():
    return datetime.now(_eu_moscow)

def get_settlement_time():
    return datetime.now(_eu_moscow).strftime('%Y-%m-%d')

schedule.every().day.at("05:00").do(clear_line, boss_id=0)

cease_continuous_run = threading.Event()
class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
        while not cease_continuous_run.is_set():
            schedule.run_pending()
            time.sleep(1)

continuous_thread = ScheduleThread()
continuous_thread.start()