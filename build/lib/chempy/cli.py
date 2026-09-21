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

import itertools
import threading
import time
import sys


def animated_loading(func, display_text:str = 'loading'):
    done = False
    def animate_loading():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write(f'\r{display_text} ' + c)
            sys.stdout.flush()
            time.sleep(0.2)
        done_text = '\rDone!'
        sys.stdout.write(f'{done_text.ljust(len(display_text) + 3)}\n')
    t = threading.Thread(target=animate_loading)
    t.start()
    r_value = func()
    done = True
    return r_value


def success_fail(op:bool):
    if op:
        print('success')
    else:
        print('failed')


def header_box(text:str, indent:int = 0) -> str:
    text = f'|  {text}  |'
    box = f'{'\n' * 2}{' ' * indent}{'-' * len(text)}{'\n'}'
    box += f'{' ' * indent}{text}{'\n'}'
    box += f'{' ' * indent}{'-' * len(text)}{'\n' * 2}'
    return box


def header_text(text:str):
    return f'{'\n' * 2}{text}\n{'=' * len(text)}\n'
