import pytest

from ..primitives import (
    sign, verify, sha256_hash, sanitize, num_digits, leading_zeros,
    pack, unpack, split_escaped, get_word_after
)


## sign

def test_sign_returns_bytes():
    result = sign(b'test data', b'secret_key_1234567890123456789012')
    assert isinstance(result, bytes)


def test_sign_length_matches_digest():
    result = sign(b'data', b'secret_key_1234567890123456789012')
    assert len(result) == 32


def test_sign_deterministic():
    key = b'secret_key_1234567890123456789012'
    assert sign(b'data', key) == sign(b'data', key)


def test_sign_different_data():
    key = b'secret_key_1234567890123456789012'
    assert sign(b'data1', key) != sign(b'data2', key)


def test_sign_different_key():
    k1 = b'key1_aaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    k2 = b'key2_aaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    assert sign(b'data', k1) != sign(b'data', k2)


def test_sign_key_too_short():
    with pytest.raises(AssertionError):
        sign(b'data', b'short')


## verify

def test_verify_valid_signature():
    key = b'secret_key_1234567890123456789012'
    data = b'test data'
    sig = sign(data, key)
    assert verify(sig, data, key) == True


def test_verify_invalid_signature():
    key = b'secret_key_1234567890123456789012'
    assert verify(b'wrong_signature_123456789012345678901', b'data', key) == False


def test_verify_tampered_data():
    key = b'secret_key_1234567890123456789012'
    sig = sign(b'original', key)
    assert verify(sig, b'tampered', key) == False


def test_verify_wrong_key():
    key1 = b'secret_key_1234567890123456789012'
    key2 = b'other_key__1234567890123456789012'
    sig = sign(b'data', key1)
    assert verify(sig, b'data', key2) == False


## sha256_hash

def test_sha256_hash_returns_str():
    assert isinstance(sha256_hash('test'), str)


def test_sha256_hash_length():
    assert len(sha256_hash('test')) == 64


def test_sha256_hash_deterministic():
    assert sha256_hash('hello') == sha256_hash('hello')


def test_sha256_hash_different_inputs():
    assert sha256_hash('hello') != sha256_hash('world')


def test_sha256_hash_known_value():
    assert sha256_hash('') == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


## sanitize

def test_sanitizes_angle_brackets():
    assert sanitize('hello <world>') == 'helloworld'


def test_sanitizes_quotes():
    assert sanitize("it's a \"test\"") == "itsatest"


def test_sanitizes_colons_and_semicolons():
    assert sanitize('user:admin;root') == 'useradminroot'


def test_sanitizes_curly_braces():
    assert sanitize('{data}') == 'data'


def test_sanitizes_leading_trailing_dots():
    assert sanitize('...filename...') == 'filename'


def test_sanitizes_leading_trailing_spaces():
    assert sanitize('  spaced  ') == 'spaced'


def test_sanitizes_control_chars():
    result = sanitize('hello\x00world')
    assert '\x00' not in result


def test_sanitizes_backslashes():
    assert sanitize('path\\to\\file') == 'pathtofile'


def test_sanitizes_pipes():
    assert sanitize('a|b|c') == 'abc'


def test_sanitize_clean_input():
    assert sanitize('valid_name') == 'valid_name'


def test_sanitize_returns_none_on_error():
    assert sanitize(None) == None


## num_digits

def test_num_digits_single():
    assert num_digits(5) == 1


def test_num_digits_multi():
    assert num_digits(12345) == 5


def test_num_digits_zero():
    assert num_digits(0) == 1


def test_num_digits_negative():
    assert num_digits(-123) == 4


## leading_zeros

def test_leading_zeros_basic():
    assert leading_zeros(5, 3) == '005'


def test_leading_zeros_no_padding_needed():
    assert leading_zeros(123, 3) == '123'


def test_leading_zeros_with_largest_number():
    assert leading_zeros(7, largest_number=999) == '007'


def test_leading_zeros_returns_none_no_args():
    assert leading_zeros(5) == None


def test_leading_zeros_number_exceeds_max():
    assert leading_zeros(1234, 3) == '1234'


## pack

def test_pack_single():
    assert pack(['one']) == 'one'


def test_pack_multiple():
    assert pack(['a', 'b', 'c']) == 'a|:|b|:|c'


def test_pack_empty_list():
    assert pack([]) == ''


def test_pack_empty_strings():
    assert pack(['', '']) == '|:|'


## unpack

def test_unpack_single():
    assert unpack('one') == ['one']


def test_unpack_multiple():
    assert unpack('a|:|b|:|c') == ['a', 'b', 'c']


def test_unpack_empty():
    assert unpack('') == ['']


def test_unpack_empty_strings():
    assert unpack('|:|') == ['', '']


def test_roundtrip():
    original = ['hello', 'world', 'test']
    assert unpack(pack(original)) == original


## split_escaped

def test_split_escaped_basic():
    assert split_escaped('a,b,c') == ['a', 'b', 'c']


def test_split_escaped_with_escape():
    assert split_escaped('a\\,b,c') == ['a,b', 'c']


def test_split_escaped_trailing_escape():
    assert split_escaped('a,b\\') == ['a', 'b\\']


def test_split_escaped_no_sep():
    assert split_escaped('hello') == ['hello']


def test_split_escaped_empty():
    assert split_escaped('') == ['']


def test_split_escaped_custom_sep():
    assert split_escaped('a;b;c', sep=';') == ['a', 'b', 'c']


def test_split_escaped_custom_escape():
    assert split_escaped('a\\;b;c', sep=';', escape='\\') == ['a;b', 'c']


def test_split_escaped_double_escape():
    assert split_escaped('a\\\\b,c') == ['a\\b', 'c']


## get_word_after

def test_get_word_after_basic():
    assert get_word_after('color ', 'The color red is nice') == 'red'


def test_get_word_after_not_found():
    assert get_word_after('missing', 'no match here') == None


def test_get_word_after_at_end():
    assert get_word_after('word ', 'last word here ') == 'here'


def test_get_word_after_special_word():
    assert get_word_after('name:', 'name:John') == 'John'


def test_get_word_after_first_match():
    assert get_word_after('key ', 'key first key second') == 'first'
