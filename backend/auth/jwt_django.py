import datetime
import jwt
from django.conf import settings

def encode_jwt(payload: dict, expire_timedelta: datetime.timedelta = None):
    private_key = settings.JWT_PRIVATE_KEY_PATH.read_text()
    algorithm = settings.JWT_ALGORITHM
    expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    to_encode = payload.copy()
    now = datetime.datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + datetime.timedelta(minutes=expire_minutes)
    to_encode.update(iat=now, exp=expire)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded

def decode_jwt(token: str):
    public_key = settings.JWT_PUBLIC_KEY_PATH.read_text()
    algorithm = settings.JWT_ALGORITHM
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded 