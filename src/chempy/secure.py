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


# Encryption and Obfuscation
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import secrets
import threading
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm
from pgpy import PGPKey, PGPUID
from chempy.rdm import random_number


def generate_aes_key(key_size:int = 256) -> bytes:
    ## Generate secure keys for AES
    if key_size == 128:
        ## 16 bytes for AES-128
        return secrets.token_bytes(16)
    elif key_size == 192:
        ## 24 bytes for AES-192
        return secrets.token_bytes(24)
    elif key_size == 256:
        ## 32 bytes for AES-256
        return secrets.token_bytes(32)
    else:
        raise ValueError('The key size must be 128, 192, or 256')


def encrypt_aes(plaintext:str, key:bytes = None) -> str:
    ## Determine if a key needs to be generated:
    key_provided = False
    if key == None: key = generate_aes_key()
    else: key_provided = True

    ## Pad plaintext to be a multiple of block size:
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    ## Create AES cipher in ECB mode:
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    ## Return Base64 encoded ciphertext:
    output = base64.b64encode(ciphertext).decode()
    if key_provided: return output
    else: return (output, key)


def decrypt_aes(ciphertext:str, key:bytes) -> str:
    ## Decode Base64 encoded ciphertext:
    ciphertext = base64.b64decode(ciphertext)

    ## Create AES cipher in ECB mode:
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    ## Unpad the data:
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    return plaintext.decode()


def asym_alpha_to_numeric(input:str) -> str:
    ## Changes text to numeric only.
    ## This is not a good obfuscation method, but it is useful for renaming files.
    codex = ['p:;/?{}[]\\\'\"|)', 'qaz!', 'wsx@', 'edc#', 'rfv$', 'tgb%', 'yhn^', 'ujm&', 'ik,<*', 'ol.>(']
    output = []
    for c in input:
        found = False
        for i in range(len(codex)):
            if c.lower() in codex[i]:
                output.append(str(i))
                found = True
                break
        if not found:
            output.append('0')
    return ''.join(output)


def generate_pgp_keypair(
        name:str = 'User',
        comment:str = 'None',
        email:str = 'email@example.com',
        password:str = None) -> tuple[str, str]:

    ## Attempt to increase entropy by generating random numbers during key creation
    def __entropy(itertions:int = 1000000):
        tmp_str = ''
        for i in range(itertions):
            tmp_str = f'{random_number()}'
    entropy_thread  = threading.Thread(target=__entropy)
    entropy_thread.start()

    ## Generate PGP key object    
    key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
    uid = PGPUID.new(name, comment=comment, email=email)
    key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications},
            hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA512],
            ciphers=[SymmetricKeyAlgorithm.AES256])

    ## Password protect the private key
    if password != None:
        key.protect(password)

    private_key = str(key)
    public_key = str(key.pubkey)
    return (private_key, public_key)


def load_key(path:str) -> PGPKey:
    key, _ = PGPKey.from_file(path)
    return key


def string_to_pgpkey(key_str:str) -> PGPKey:
    key, _ = PGPKey.from_blob(key_str)
    return key


def generate_password(
        length:int = 16,
        use_lowercase:bool = True,
        use_uppercase:bool = True,
        use_numbers:bool = True,
        use_symbols:bool = False,
        charset:str = None) -> str:
    lowercase = list('abcdefghijklmnopqrstuvwxyz')
    uppercase = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list(r'!@#$%^&*()_+-=,.<>/?;:\'"[]{}|`~')
    #print(symbols)
    if charset != None:
        options = list(charset)
    else:
        options = []
        if use_lowercase:
            options.extend(lowercase)
        if use_uppercase:
            options.extend(uppercase)
        if use_numbers:
            options.extend(numbers)
        if use_symbols:
            options.extend(symbols)
    max_option = (len(options) - 1)
    #print(options)
    #print(max_option)
    if max_option == -1:
        return 'password'
    output = []
    for i in range(length):
        output.append(options[random_number(max_number=max_option)])
    #print(output)
    output = ''.join(output)
    return output
