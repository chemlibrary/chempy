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

import hashlib
import hmac
import re


def sign(data: bytes, key: bytes, algorithm=hashlib.sha256) -> bytes:
    try:
        assert len(key) >= algorithm().digest_size, (
            "Key must be at least as long as the digest size of the hashing algorithm!"
        )
        return hmac.new(key, data, algorithm).digest()
    except:
        raise
        return None


def verify(signature: bytes, data: bytes, key: bytes, algorithm=hashlib.sha256) -> bytes:
    try:
        expected = sign(data, key, algorithm)
        return hmac.compare_digest(expected, signature)
    except:
        raise
        return None


def sha256_hash(item: str) -> str:
    try:
        hash = hashlib.new('sha256')
        hash.update(item.encode())
        return hash.hexdigest()
    except:
        raise
        return None


def sanitize(dirty:str) -> str:
    """
    Cleans a string.
    """
    invalid_chars = r'[ <>:;"/\\\'`{}|+\x00-\x1f]'
    try:
        clean = re.sub(invalid_chars, '', dirty)
        return clean.strip(' .')
    except:
        return None


def num_digits(number:int) -> int:
    return len(str(number))


def leading_zeros(number:int, max_digits:int = None, largest_number:int = None) -> str:
    """
    Returns 'number' with leading zeros.
    Specify either the 'max_digits' or the 'largest_number' in the series.
    """
    if max_digits == None and largest_number == None:
        return None
    if largest_number != None:
        max_digits = len(str(largest_number))
    num_leading_zeros = int(max_digits - len(str(number)))
    return ('0' * num_leading_zeros) + str(number)


def pack(contents:list[str]) -> str:
    return '|:|'.join(contents)


def unpack(contents:str) -> list[str]:
    return contents.split('|:|')


def split_escaped(s:str, sep:str = ',', escape:str = '\\') -> list[str]:
    parts = []
    buf = []
    escaped = False

    for ch in s:
        if escaped:
            # always take char literally
            buf.append(ch)
            escaped = False
            continue

        if ch == escape:
            escaped = True
            continue

        if ch == sep:
            parts.append(''.join(buf))
            buf = []
            continue

        buf.append(ch)

    if escaped:
        # trailing escape — keep it literally
        buf.append(escape)
    parts.append(''.join(buf))
    return parts



def get_word_after(word_after:str, full_text:str):
    pattern = rf"(?<={re.escape(word_after)})\S+"
    m = re.search(pattern, full_text)
    token = m.group(0) if m else None
    return token

