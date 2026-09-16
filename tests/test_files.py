import os
import tempfile
import pytest
from pathlib import Path

from chempy.files import (
    clean_path, is_child_of_dir, file_read, file_read_lines, file_write,
    file_append, file_exists, file_delete, file_safe_write, file_size,
    dir_size, human_size, unixfy_file_seps, file_name, file_extension,
    file_name_hash, file_hash, dir_contents, parent_path,
    sanitize_filename, sanitize_path, validate_and_resolve_path,
    file_safe_copy
)


@pytest.fixture
def tmp_file():
    path = os.path.join(tempfile.gettempdir(), 'test_files_py.txt')
    yield path
    if file_exists(path):
        file_delete(path)


@pytest.fixture
def tmp_dir():
    path = os.path.join(tempfile.gettempdir(), 'test_files_py_dir')
    os.makedirs(path, exist_ok=True)
    yield path
    if os.path.exists(path):
        import shutil
        shutil.rmtree(path, ignore_errors=True)


## clean_path

def test_clean_path_normalizes():
    result = clean_path('/tmp/../tmp/foo')
    assert os.path.join('tmp', 'foo') in result or 'foo' in result


def test_clean_path_returns_absolute():
    result = clean_path('relative/path')
    assert os.path.isabs(result)


## is_child_of_dir

def test_is_child_of_dir_true():
    assert is_child_of_dir('/parent/child', '/parent') == True


def test_is_child_of_dir_same_path():
    assert is_child_of_dir('/parent', '/parent') == True


def test_is_child_of_dir_false():
    assert is_child_of_dir('/other/path', '/parent') == False


def test_is_child_of_dir_sibling():
    assert is_child_of_dir('/parent/sibling', '/parent/child') == False


## file_read

def test_file_read_text(tmp_file):
    file_write(tmp_file, 'hello world')
    assert file_read(tmp_file) == 'hello world'


def test_file_read_hex(tmp_file):
    file_write(tmp_file, 'AB')
    result = file_read(tmp_file, hex=True)
    assert result == '4142'


def test_file_read_nonexistent():
    with pytest.raises(FileNotFoundError):
        file_read('/nonexistent/path/that/does/not/exist.txt')


## file_read_lines

def test_file_read_lines(tmp_file):
    file_write(tmp_file, 'line1\nline2\nline3')
    assert file_read_lines(tmp_file) == ['line1', 'line2', 'line3']


## file_write and file_append

def test_file_write(tmp_file):
    assert file_write(tmp_file, 'test content') == True
    assert file_read(tmp_file) == 'test content'


def test_file_append(tmp_file):
    file_write(tmp_file, 'first')
    file_append(tmp_file, ' second')
    assert file_read(tmp_file) == 'first second'


## file_exists

def test_file_exists_true(tmp_file):
    file_write(tmp_file, 'exists')
    assert file_exists(tmp_file) == True


def test_file_exists_false():
    assert file_exists('/nonexistent/file.txt') == False


## file_delete

def test_file_delete(tmp_file):
    file_write(tmp_file, 'delete me')
    assert file_delete(tmp_file) == True
    assert file_exists(tmp_file) == False


def test_file_delete_nonexistent():
    assert file_delete('/nonexistent/file.txt') == None


## file_safe_write

def test_file_safe_write(tmp_file):
    assert file_safe_write(tmp_file, 'safe content') == True
    assert file_read(tmp_file) == 'safe content'


def test_file_safe_write_creates_dirs(tmp_file):
    nested = os.path.join(os.path.dirname(tmp_file), 'nested_dir', 'test.txt')
    assert file_safe_write(nested, 'nested content') == True
    assert file_read(nested) == 'nested content'
    file_delete(nested)
    os.rmdir(os.path.join(os.path.dirname(tmp_file), 'nested_dir'))


## file_size

def test_file_size(tmp_file):
    content = 'size test content'
    file_write(tmp_file, content)
    assert file_size(tmp_file) == len(content)


## dir_size

def test_dir_size(tmp_dir):
    file_write(os.path.join(tmp_dir, 'a.txt'), '12345')
    file_write(os.path.join(tmp_dir, 'b.txt'), '1234567890')
    assert dir_size(tmp_dir) == 15


## human_size

def test_human_size_zero():
    assert human_size(0) == '0B'


def test_human_size_bytes():
    assert human_size(500) == '500.00 B'


def test_human_size_kb():
    assert human_size(1024) == '1.00 KB'


def test_human_size_mb():
    assert human_size(1048576) == '1.00 MB'


## unixfy_file_seps

def test_unixfy_file_seps():
    assert unixfy_file_seps('C:\\Users\\test') == 'C:/Users/test'


def test_unixfy_file_seps_already_unix():
    assert unixfy_file_seps('/home/user/test') == '/home/user/test'


## file_name

def test_file_name_with_ext():
    assert file_name('/path/to/file.txt') == 'file.txt'


def test_file_name_without_ext():
    assert file_name('/path/to/file.txt', include_extension=False) == 'file'


def test_file_name_no_ext():
    assert file_name('/path/to/Makefile', include_extension=False) == 'Makefile'


## file_extension

def test_file_extension():
    assert file_extension('/path/to/file.txt') == '.txt'


def test_file_extension_no_ext():
    assert file_extension('/path/to/Makefile') == ''


## file_name_hash

def test_file_name_hash():
    hash1 = file_name_hash('/path/to/test.txt')
    hash2 = file_name_hash('/other/path/test.txt')
    assert hash1 == hash2
    assert len(hash1) == 64


## file_hash

def test_file_hash_sha256(tmp_file):
    file_write(tmp_file, 'hash test')
    result = file_hash(tmp_file)
    assert len(result) == 64


def test_file_hash_consistency(tmp_file):
    file_write(tmp_file, 'consistent hash')
    h1 = file_hash(tmp_file)
    h2 = file_hash(tmp_file)
    assert h1 == h2


def test_file_hash_different_content(tmp_file):
    file_write(tmp_file, 'content A')
    h1 = file_hash(tmp_file)
    file_write(tmp_file, 'content B')
    h2 = file_hash(tmp_file)
    assert h1 != h2


## dir_contents

def test_dir_contents(tmp_dir):
    file_write(os.path.join(tmp_dir, 'a.txt'), '')
    file_write(os.path.join(tmp_dir, 'b.txt'), '')
    contents = dir_contents(tmp_dir)
    assert len(contents) == 2


def test_dir_contents_filenames_only(tmp_dir):
    file_write(os.path.join(tmp_dir, 'test.txt'), '')
    contents = dir_contents(tmp_dir, filenames_only=True)
    assert contents == ['test.txt']


def test_dir_contents_recursive(tmp_dir):
    subdir = os.path.join(tmp_dir, 'sub')
    os.makedirs(subdir)
    file_write(os.path.join(subdir, 'nested.txt'), '')
    contents = dir_contents(tmp_dir, recursive=True)
    assert len(contents) == 1


def test_dir_contents_exclude(tmp_dir):
    file_write(os.path.join(tmp_dir, 'keep.txt'), '')
    file_write(os.path.join(tmp_dir, 'skip.txt'), '')
    contents = dir_contents(tmp_dir, exclude_files=['skip.txt'])
    assert len(contents) == 1
    assert all('skip.txt' not in c for c in contents)


## parent_path

def test_parent_path():
    result = parent_path('/home/user/docs')
    assert 'home' in result and 'user' in result


def test_parent_path_root():
    result = parent_path('/home')
    assert result.endswith(os.sep) or len(result) <= 3


## sanitize_filename

def test_sanitize_filename_removes_invalid():
    result = sanitize_filename('file<name>.txt')
    assert '<' not in result
    assert '>' not in result


def test_sanitize_filename_safe():
    result = sanitize_filename('valid_filename.txt')
    assert result == 'valid_filename.txt'


## sanitize_path

def test_sanitize_path_removes_invalid():
    result = sanitize_path('/path/with<invalid>chars')
    assert '<' not in result
    assert '>' not in result


def test_sanitize_path_normalizes():
    result = sanitize_path('/tmp/../tmp/foo')
    assert '..' not in result


## validate_and_resolve_path

def test_validate_and_resolve_path_valid():
    base = tempfile.gettempdir()
    result = validate_and_resolve_path(base, 'test.txt')
    assert str(result).startswith(base)


def test_validate_and_resolve_path_traversal():
    base = tempfile.gettempdir()
    with pytest.raises(PermissionError):
        validate_and_resolve_path(base, '../../etc/passwd')


## file_safe_copy

def test_file_safe_copy(tmp_file, tmp_dir):
    file_write(tmp_file, 'copy test content')
    dest = os.path.join(tmp_dir, 'copied.txt')
    result = file_safe_copy(tmp_file, dest)
    assert file_read(str(dest)) == 'copy test content'
    assert Path(str(dest)).exists()


def test_file_safe_copy_creates_dirs(tmp_file, tmp_dir):
    nested_dest = os.path.join(tmp_dir, 'nested', 'dir', 'copied.txt')
    file_write(tmp_file, 'nested copy')
    result = file_safe_copy(tmp_file, nested_dest)
    assert file_read(nested_dest) == 'nested copy'
