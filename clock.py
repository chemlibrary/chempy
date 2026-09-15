import time
from datetime import datetime


def dtstr() -> str:
    now = datetime.now()
    formatted_date_time = now.strftime('%Y%m%d%H%M%S')
    return formatted_date_time


def tsstr() -> str:
    now = datetime.now()
    formatted_time = now.strftime('%Y%m%d:%H%M%S.%f')
    return formatted_time


class Timer:
    def __init__(self):
        self.start_time:float = time.time()
        self.stop_time:float = None
        self.duration:float = 0.0
    def start(self) -> bool:
        self.start_time = time.time()
        self.stop_time = None
        self.duration = 0.0
        return self.start_time
    def stop(self) -> bool:
        self.stop_time = time.time()
        self.duration = self.stop_time - self.start_time
        return self.stop_time
    def status(self) -> str:
        if self.duration == 0.0:
            return f'{round((self.stop_time - self.start_time), 4)}s'
        return f'{round(self.duration, 4)}s'
    def time(self) -> float:
        return (time.time() - self.start_time)
    def started(self):
        return self.start_time
    def stopped(self):
        return self.stop_time
