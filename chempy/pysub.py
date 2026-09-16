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
