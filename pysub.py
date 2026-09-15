import subprocess
import sys


def pysub(script:str, args_list=[]):
    #args_list = ["arg1", "arg2"]

    # Use same Python interpreter
    cmd = [sys.executable, script] + args_list

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    error = result.stderr
    code = result.returncode

    if output == '':
        output = error

    return {'output': output, 'error': error, 'code': code}


def shsub(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout
    error = result.stderr
    code = result.returncode

    if output == '':
        output = error

    return {'output': output, 'error': error, 'code': code}
