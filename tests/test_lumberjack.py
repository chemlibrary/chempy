import os
import time

import pytest
from ..lumberjack import Lumberjack, Log
from ..files import file_exists, file_delete, file_write, file_read, file_append

### test_use_existing_log doesn't properly clean up if you don't use a background thread (this seems improper)

def __cleanup(obj):
    path = obj.log_path
    obj.exit()
    return file_delete(path)


def __existing_log_file(test_log_path: str) -> bool:
    if not file_exists(test_log_path):
        return file_write(path=test_log_path, contents='Existing Log Line')
    return True


def test_create_lumberjack_object():
    logger = Lumberjack(create=False, background_thread=False)
    assert isinstance(logger, Lumberjack)


def test_create_log_object():
    logger = Lumberjack(create=False, background_thread=False)
    log = Log(logger=logger, text='Test Event!')
    assert isinstance(log, Log)


def test_use_existing_log():
    test_log = 'existing_log_TEST.log'
    __existing_log_file(test_log)
    logger = Lumberjack(create=False, log_path=test_log)
    logger.log('event')
    time.sleep(logger.background_thread_poll_rate + 1)
    assert len(file_read(logger.log_path).split('\n')) >= 1
    __cleanup(logger)


def test_background_thread():
    test_log = 'background_thread_TEST.log'
    __existing_log_file(test_log)
    logger = Lumberjack(log_path=test_log)
    logger.log('event 1')
    time.sleep(logger.background_thread_poll_rate + 1)
    assert len(file_read(logger.log_path).split('\n')) > 1
    __cleanup(logger)


def test_write_to_log_on_exit():
    test_log = 'write_to_log_on_exit_TEST.log'
    __existing_log_file(test_log)
    logger = Lumberjack(log_path=test_log)
    logger.log('This line should be saved to file on exit')
    time.sleep(logger.background_thread_poll_rate + 1)
    assert len(file_read(logger.log_path).split('\n')) > 1
    __cleanup(logger)


def test_create_and_cleanup_woodpile():
    test_log = 'create_and_cleanup_woodpile_TEST.log'
    __existing_log_file(test_log)
    logger = Lumberjack(log_path=test_log)
    logger.log('This line was added directly from lumberjack.')
    logger.create_woodpile()
    assert file_exists(logger.woodpile.path) and file_exists(logger.woodpile.script_path)
    __cleanup(logger)


def test_add_from_woodpile():
    test_log = 'add_from_woodpile_TEST.log'
    __existing_log_file(test_log)
    logger = Lumberjack(log_path=test_log)
    logger.log('This line was added directly from lumberjack.')
    logger.create_woodpile()
    file_append(logger.woodpile.path, 'This line was added from the woodpile.')
    time.sleep(logger.background_thread_poll_rate + 2)
    assert len(file_read(logger.log_path).split('\n')) == 3
    __cleanup(logger)


def test_woodpile_script():
    test_log = 'woodpile_script_TEST.log'
    __existing_log_file(test_log)
    logger = Lumberjack(log_path=test_log)
    logger.log('This line was added directly from lumberjack.')
    logger.create_woodpile()
    os.system(f'python {logger.woodpile.script_path} "This line was added from the woodpile script."')
    time.sleep(logger.background_thread_poll_rate + 1)
    assert len(file_read(logger.log_path).split('\n')) == 3
    __cleanup(logger)


if __name__ == '__main__':
    pytest.main()
