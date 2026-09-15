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
