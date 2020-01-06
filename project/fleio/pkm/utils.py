import base64
import hashlib
import re
import binascii
from django.conf import settings
from django.utils.encoding import force_text
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def is_valid_ssh_public_key(public_key):
    """
    This method is mainly used to validate http input.
    We therfore force the conversion to text below.
    :param public_key: The SSH public key (string) introduced by the user
    :return: True if a valid ssh-public-key was given, False otherwise
    References: security.stackexchange.com/questions/42268/how-do-i-get-the-rsa-bit-length-with-the-pubkey-and-openssl
                docs.python.org/2/library/base64.html
                cryptopp.com/wiki/Keys_and_Formats

    """
    public_key = force_text(public_key)  # Py2 and Py3 compatibility
    regex_pattern = re.compile(r"(ssh-(dss|rsa|ed25519)|ecdsa-sha2-nistp\d{3}) * (?P<key>AAAA[^ \n]+)( [^ ]*)*")

    if regex_pattern.match(public_key) is None:
        return False

    found_string = regex_pattern.search(public_key)
    key = found_string.group('key')
    try:
        base64.b64decode(key)
    except TypeError:
        return False
    except binascii.Error:
        return False

    return True


def get_fingerprint(key):
    key = base64.b64decode(key.strip().split()[1].encode('ascii'))
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))


def generate_key_pair(bits=2048):
    """
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    """
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=bits
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        getattr(settings, 'SSH_PRIVATE_KEY_FORMAT', crypto_serialization.PrivateFormat.TraditionalOpenSSL),
        crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    return public_key, private_key
