import os
import argparse
from pathlib import Path
from chempy.cli import success_fail
from chempy.files import (
    file_read,
    file_safe_write,
    file_hash,
    file_name_hash,
    file_size,
    parent_path,
    dir_contents)
from chempy.primitives import sha256_hash




## Create ledger file contents for the specified library.
def make_ledger_contents(library_path: str = '.', librarian_name: str = 'librarian') -> str:

    ## Get a recursive list of files in the 'library_path' directory.
    files = dir_contents(path = library_path, recursive = True, exclude_files = [f'.{librarian_name}'])

    ## Create list each file's hash values.
    contents = []
    for i in range(len(files)):
        contents.append(f'{file_name_hash(files[i])} {file_hash(files[i])} {file_size(files[i])}')

    ## Join list of hashes into a string.
    contents = '\n'.join(contents)

    ## Create the ledger hash.
    hashed_list = sha256_hash(contents)

    return f'{hashed_list}\n{contents}'



## Create a ledger file for the specified library.
def make_ledger_file(library_path:str = '.', ledger_path:str = None, librarian_name: str = 'librarian') -> bool:

    ## Fallback to defualt behavior if 'ledger_path' isn't specified.
    if ledger_path == None:
        ledger_path = f'{library_path}{os.sep}.{librarian_name}{os.sep}ledger'

    ## Create the ledger parent directory if it doesn't already exist.
    ledger_parent_dir = parent_path(ledger_path)
    if not os.path.isdir(ledger_parent_dir):
        os.makedirs(ledger_parent_dir)

    ## Attempt to write the ledger file, return False if the write fails.
    try:
        return file_safe_write(ledger_path, make_ledger_contents(library_path))
    except:
        return False



## Verify the specified ledger file matches the specified library contents.
def verify_library(library_path:str = '.', ledger_path:str = None, librarian_name: str = 'librarian') -> bool:

    ## Fallback to defualt behavior if 'ledger_path' isn't specified.
    if ledger_path == None:
        ledger_path = f'{library_path}{os.sep}.{librarian_name}{os.sep}ledger'

    ## Check that the generated ledger matches the in place ledger.
    return make_ledger_contents(library_path) == file_read(ledger_path)



## Verify the specified ledger hash matches the hash in the specified ledger file.
def verify_ledger(library_path:str = '.', ledger_path:str =  None, ledger_hash: str = None, librarian_name: str = 'librarian'):

    ## Fallback to defualt behavior if 'ledger_path' isn't specified.
    if ledger_path == None:
        ledger_path = f'{library_path}{os.sep}.{librarian_name}{os.sep}ledger'

    ## Read the ledger hash from the first line of the ledger.
    try:
        with open(ledger_path) as f:
            retrieved_ledger_hash = f.readline()
    except:
        retrieved_ledger_hash = None

    ## If no ledger hash was specified, return the ledger hash from the specified ledger.
    if ledger_hash == None:
        return retrieved_ledger_hash
    return ledger_hash == retrieved_ledger_hash



## Write content to a specified file only if the library is verified.
def add_content(content_path:str, content:str = '', library_path:str = '.', ledger_path:str = None, librarian_name: str = 'librarian') -> bool:
    if ledger_path == None:
        ledger_path = f'.{os.sep}.{librarian_name}{os.sep}ledger'
    if os.path.exists(ledger_path):
        if verify_library(library_path):
            if file_safe_write(content_path, content):
                if make_ledger_file(library_path):
                    return True
    return False






def main():
    parser = argparse.ArgumentParser(
        prog='librarian.py',
        description='Ensure the integrity of files over time.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--make_ledger', help='make a new ledger file.', default=False, action='store_true')
    group.add_argument('-c', '--make_ledger_contents', help='make and print ledger file contents.', default=False, action='store_true')
    group.add_argument('-v', '--verify_library', help='verify library matches ledger file.', default=False, action='store_true')
    group.add_argument('-k', '--verify_ledger', help='verify ledger file hash matches. print ledger file hash if no ledger hash is supplied.', default=False, action='store_true')
    parser.add_argument('-s', '--ledger_hash', help='ledger file hash.', default=None, action='store')
    parser.add_argument('-l', '--library_path', help='path of directory containing a library.', default='.', action='store')
    parser.add_argument('-p', '--ledger_path', help='path of a ledger file.', default=None, action='store')
    parser.add_argument('-d', '--librarian_name', help='name of created librarian directories.', default='.librarian', action='store')
    args = parser.parse_args()

    if args.make_ledger:
        success_fail(make_ledger_file(library_path = args.library_path, ledger_path = args.ledger_path, librarian_name = args.librarian_name))
    elif args.make_ledger_contents:
        print(make_ledger_contents(library_path = args.library_path, librarian_name = args.librarian_name))
    elif args.verify_library:
        success_fail(verify_library(library_path = args.library_path, ledger_path = args.ledger_path, librarian_name = args.librarian_name))
    elif args.verify_ledger:
        if args.ledger_hash == None:
            print(verify_ledger(library_path = args.library_path, ledger_path = args.ledger_path, librarian_name = args.librarian_name))
        else:
            success_fail(verify_ledger(ledger_path = args.ledger_path, ledger_hash = args.ledger_hash, librarian_name = args.librarian_name))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()