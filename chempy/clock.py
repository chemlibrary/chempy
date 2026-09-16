# This file is part of ChemPy.
# Copyright (C) 2026 Chem
#
# ChemPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ChemPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ChemPy. If not, see <http://www.gnu.org/licenses/>.

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
