# Commonly used bash snippets

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

