import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

from django.utils.encoding import force_bytes, force_text
from django.conf import settings


def derive_fernet_key(key):
    backend = default_backend()
    salt = b'fleio-hkdf-salt'  # NOTE(tomo): We need a predictable salt, do not change
    info = b'fleio-fernet-hkdf'
    hkdf = HKDF(algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                info=info,
                backend=backend)
    return base64.urlsafe_b64encode(hkdf.derive(force_bytes(key)))


def fernet_encrypt(value):
    value = force_bytes(value)
    key = derive_fernet_key(settings.SECRET_KEY)
    f = Fernet(key)
    return force_text(f.encrypt(force_bytes(value)))


def fernet_decrypt(value):
    key = derive_fernet_key(settings.SECRET_KEY)
    f = Fernet(key)
    return force_text(f.decrypt(force_bytes(value)))
