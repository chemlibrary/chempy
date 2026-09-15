import os
import hashlib
import re
import tempfile
import shutil
from pathlib import Path
from tqdm import tqdm


def clean_path(path:str) -> str:
    try:
        normalized_path = os.path.normpath(path)
        absolute_path = os.path.abspath(normalized_path)
        return absolute_path
    except:
        raise
        return None



def is_child_of_dir(path:str, dir:str) -> bool:
    ## Determines if path is a child of dir or is dir.

    ## Normalize the target path:
    path = os.path.abspath(path)
    ## Normalize the directory path:
    dir = os.path.abspath(dir)
    ## Check if target_path starts with directory and ensure proper trailing slash handling:
    if path == dir or path.startswith(dir + os.sep) or path.startswith(dir + '/'):
        return True
    return False



def file_read(path:str, hex:bool = False, fallback_hex:bool = True, fallback:bool = True) -> str:
    """
    Read the contents of a file.

    Args:
        path (str): The path of the file to read.
        hex (bool): Return a hex representation of the file contents.
        fallback_hex (bool): When falling back on reading bytes, return the contents as a hex string.
        fallback (bool): When reading as plaintext fails, attempt to read as bytes.

    Returns:
        str: The contents of the file, or None if errors are encountered.

    Raises:
        Exception: Any exception will be raised.
    """
    if hex:
        try:
            with open(path, 'rb') as file: contents = file.read()
            return contents.hex()
        except:
            raise
            return None
    try:
        with open(path, 'r') as file: contents = file.read()
        return contents
    except:
        if fallback: pass
        else:
            raise
            return None
    try:
        with open(path, 'rb') as file: contents = file.read()
        if fallback_hex: contents = contents.hex()
        return contents
    except:
        raise
        return None
def file_read_lines(path:str) -> list[str]:
    try:
        contents = file_read(path)
        if contents == None:
            return None
        return contents.split('\n')
    except:
        raise
        return None



def file_write(path:str, contents:str = '') -> bool:
    try:
        with open(path, 'w') as f:
            f.write(contents)
        return True
    except:
        raise
        return False



def file_append(path:str, contents:str = '') -> bool:
    try:
        with open(path, 'a') as f:
            f.write(contents)
        return True
    except:
        raise
        return False



def file_exists(path:str):
    return os.path.exists(path)



def file_delete(path:str) -> bool:
    if not os.path.isfile(path) and not os.path.isdir(path):
        return None
    
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            os.rmdir(path)
        return True
    except:
        raise
        return False



def file_safe_write(path:str, contents:str, encoding:str = 'utf-8'):
    """
    Writes content to a file atomically to prevent data corruption.
    """
    target_path = Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding=encoding,
            dir=target_path.parent,
            delete=False,
            suffix='.tmp'
        ) as tmp_file:
            tmp_file.write(contents)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
            temp_path = tmp_file.name
        shutil.move(temp_path, target_path)
        return True
    except:
        raise
        return False



def file_size(path:str) -> str:
    try:
        with open(path, 'r') as file:
            old_file_position = file.tell()
            file.seek(0, 2)
            size = file.tell()
            file.seek(old_file_position, 0)
            return size
    except:
        raise
        return None



def dir_size(path:str = '.'):
    """
    Calculates the total size of a directory and all its subdirectories.
    """
    try:
        path = Path(path)
        size = 0
        for p in path.rglob('*'):
            if p.is_file():
                try:
                    size += p.stat().st_size
                except (PermissionError, FileNotFoundError):
                    continue
        return size
    except:
        raise
        return None



def human_size(size_bytes:int):
    """
    Formats size in bytes to a human-readable string with units.
    """
    if size_bytes <= 0:
        return "0B"
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {units[i]}"


def unixfy_file_seps(path:str) -> str:
    return path.replace('\\', '/')



def file_name(path:str, include_extension:bool = True) -> str:
    try:
        base_name = os.path.basename(path)
        if include_extension or not '.' in base_name:
            return base_name
        name, ext = os.path.splitext(base_name)
        return name
    except:
        raise
        return None



def file_extension(path:str) -> str:
    try:
        extension = ''
        parts = path.split('.')
        if len(parts) > 1:
            extension = '.' + parts[-1]
        return extension
    except:
        raise
        return None



def file_name_hash(path: str) -> str:
    try:
        name = os.path.basename(path)
        hash = hashlib.new('sha256')
        hash.update(name.encode())
        return hash.hexdigest()
    except:
        raise
        return None



def file_hash(path:str, algorithm:str = 'sha256', chunk_size:int = 65536) -> str:
    """
    Calculates the hash of a file.
    """
    try:
        hash = hashlib.new(algorithm)
        with Path(path).open('rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash.update(chunk)
        return hash.hexdigest()
    except:
        raise
        return None



def dir_contents(path:str = '.', filenames_only:bool = False, recursive = False, exclude_files:list[str] = None, lazy_exclude:bool = False) -> list[str]:
    try:
        path = os.path.abspath(path)
        items = []
        with os.scandir(path) as library:
            for item in library:
                if exclude_files != None:
                    exclude_it = False
                    if os.path.basename(item.path) in exclude_files:
                        exclude_it = True
                    elif lazy_exclude:
                        for exclusion in exclude_files:
                            if exclusion in item.path:
                                exclude_it = True
                                break
                    if exclude_it:
                        continue
                if not recursive or item.is_file():
                    if filenames_only:
                        items.append(os.path.basename(item.path))
                    else:
                        items.append(item.path)
                elif item.is_dir():
                    items.extend(dir_contents(path = item.path, filenames_only = filenames_only, exclude_files = exclude_files, recursive = recursive))
        return items
    except:
        raise
        return None



def parent_path(path:str = '.') -> str:
    try:
        path = os.path.abspath(path)
        path_components = path.rsplit(os.sep, 1)
        parent_path = path_components[0]
        if parent_path == '':
            return os.sep
        return parent_path
    except:
        raise
        return None



def sanitize_filename(filename:str, replacement_char:str = '_') -> str:
    """
    Cleans a filename so that it's safe for any OS.
    """

    invalid_chars = r'[ <>:;"/\\\'`!@#$%^&*{}|,+=?\x00-\x1f]'

    try:
        sanitized = re.sub(invalid_chars, replacement_char, filename)
        return sanitized.strip(' .')
    except:
        raise
        return None



def sanitize_path(path:str, replacement_char:str = '') -> str:
    """
    Cleans a path so it's a valid and safe path for any OS.
    """

    invalid_chars = r'[ <>;"\'`!@#$%^&*{}|,+=?\x00-\x1f]'
    try:
        sep_cleaned = re.sub(r'\\', '/', path)
        sanitized = re.sub(invalid_chars, replacement_char, sep_cleaned)
        stripped = sanitized.strip(' .')
        normalized = os.path.normpath(stripped)
        absolute = os.path.abspath(normalized)
        return absolute
    except:
        raise
        return None



def validate_and_resolve_path(base_dir:str, dirty_path:str):
    """
    Safely resolves a path, ensuring it stays within a base directory.
    This is critical for preventing directory traversal attacks.
    """
    base_dir = Path(base_dir).resolve()

    # create a canonical, absolute path, removing '..' segments
    resolved_path = (base_dir / dirty_path).resolve()

    # check if the resolved_path is still inside the base_dir
    if resolved_path.is_relative_to(base_dir):
        return resolved_path
    else:
        raise PermissionError("Path traversal attempt detected!")



def file_safe_copy(source:str, destination:str):
    """
    Copies a file and verifies the copy's integrity, deleting the copy if verification fails.
    """
    source_path, destination_path = Path(source), Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    source_size = source_path.stat().st_size
    source_hash = file_hash(source_path)

    with (source_path.open('rb') as fsource,
            destination_path.open('wb') as fdestination):
        shutil.copyfileobj(fsource, fdestination, length=16*1024*1024)

    destination_hash = file_hash(destination_path)

    if source_hash != destination_hash:
        destination_path.unlink()
        raise IOError(f"Verification failed! Hashes do not match for {destination_path}")

    return destination_path



def file_safe_copy_cli(source:str, destination:str):
    """
    Copies a file with a progress bar and verifies the copy's integrity, deleting the copy if verification fails.
    """
    source_path, destination_path = Path(source), Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    source_size = source_path.stat().st_size
    print(f"Calculating hash for {source_path.name}...")
    source_hash = file_hash(source_path)

    print(f"Copying {source_path.name} to {destination_path}...")
    with (source_path.open('rb') as fsource,
        destination_path.open('wb') as fdestination,
        tqdm(total=source_size, unit='B', unit_scale=True, desc=source_path.name) as pbar):
            shutil.copyfileobj(fsource, fdestination, length=16*1024*1024)
            pbar.n = source_size
            pbar.refresh()

    print("Verifying copy...")
    destination_hash = file_hash(destination_path)

    if source_hash != destination_hash:
        destination_path.unlink()
        raise IOError(f"Verification failed! Hashes do not match for {destination_path}")

    print(f"Success! {destination_path.name} copied and verified.")
    return destination_path

