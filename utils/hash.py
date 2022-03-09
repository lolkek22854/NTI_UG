import uuid
import hashlib


def hash_password(password):
    # uuid используется для генерации случайного числа
    salt = uuid.uuid4().hex
    return hashlib.sha256(
        salt.encode() + password.encode()).hexdigest()[:16]
