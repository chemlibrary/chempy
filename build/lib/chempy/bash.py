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

def require_sudo(required:bool = False) -> str:
    if required:
        return 'if [[ $(/usr/bin/id -u) -ne 0 ]]; then\n    echo "This script must be run with sudo. Exiting..."\n    exit\nfi\n'
    else:
        return ''


def shebang(location:str = None) -> str:
    if location == None:
        location = '/bin/bash'
    return f'#!{location}\n'


def build_script_reqs(sudo_required:bool = False, interpreter_location:str = None) -> str:
    return f'{shebang(interpreter_location)}{require_sudo(sudo_required)}'

