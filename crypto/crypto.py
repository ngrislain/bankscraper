import random
import struct
import base64
import hashlib
import warnings
from StringIO import StringIO

def check_output(cmd, input_=None, *popenargs, **kwargs):
    """Custom variant of stdlib's check_output(), but with stdin feed support."""
    from subprocess import Popen, PIPE, CalledProcessError
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    stdin = None
    if input_ is not None:
        stdin = PIPE
    process = Popen(stdout=PIPE, stdin=stdin, *((cmd,) + popenargs), **kwargs)
    output, unused_err = process.communicate(input_)
    retcode = process.poll()
    if retcode:
        raise CalledProcessError(retcode, ' '.join(cmd), output=output)
    return output

def _random_noise(len):
    return ''.join(chr(random.randint(0, 0xFF)) for i in range(len))

class AES(object):
    def __init__(self, password):
        # First, generate a fixed-length key of 32 bytes (for AES-256)
        self._password = password

    def encrypt(self, string):
        """Encrypts a string using AES-256."""
        try:
            envvar = hashlib.sha256(_random_noise(16)).hexdigest()
            ciphertext = check_output([
                'openssl', 'enc', '-e', '-aes-256-cbc', '-a',
                '-salt', '-pass', 'env:{0}'.format(envvar)],
                input_=string,
                env={envvar: self._password})
            return ciphertext.strip()
        except:
            raise RuntimeError('Could not encrypt.')

    def decrypt(self, b64_ciphertext):
        """Decrypts a string using AES-256."""
        try:
            envvar = hashlib.sha256(_random_noise(16)).hexdigest()
            plaintext = check_output([
                'openssl', 'enc', '-d', '-aes-256-cbc', '-a', '-pass',
                'env:{0}'.format(envvar)],
                input_=b64_ciphertext + '\n',
                env={envvar: self._password})
            return plaintext
        except:
            raise RuntimeError('Could not decrypt.')

if __name__ == '__main__':
    aes = AES('password ok')
    enc = aes.encrypt('string ok')
    print enc
    print aes.decrypt(enc)