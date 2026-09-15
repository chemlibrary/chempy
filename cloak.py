# Encryption and Obfuscation
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import secrets


def generate_aes_key(key_size:int = 256) -> bytes:
    ## Generate secure keys for AES
    if key_size == 128:
        return secrets.token_bytes(16)  # 16 bytes for AES-128
    elif key_size == 192:
        return secrets.token_bytes(24)  # 24 bytes for AES-192
    elif key_size == 256:
        return secrets.token_bytes(32)  # 32 bytes for AES-256
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
