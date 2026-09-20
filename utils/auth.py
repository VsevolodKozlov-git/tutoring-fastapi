import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash

_env_path = Path(__file__).resolve().parent.parent / '.env.main'
load_dotenv(_env_path)


@dataclass(frozen=True)
class AuthConfig:
    SECRET_KEY: str
    ALGORITHM: str
    EXP_DATE: int


auth_config = AuthConfig(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    ALGORITHM=os.getenv('ALGORITHM', 'HS256'),
    EXP_DATE=int(os.getenv('EXP_DATE', '3600')),
)

_password_hasher = PasswordHash.recommended()

_security = HTTPBearer()


def get_token(data: dict) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        **data,
        'iat': now,
        'exp': now + timedelta(seconds=auth_config.EXP_DATE),
    }
    return jwt.encode(payload, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)


def decode_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_security)],
) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials,
            auth_config.SECRET_KEY,
            algorithms=[auth_config.ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return payload


def get_hashed_password(password: str) -> str:
    return _password_hasher.hash(password)


def is_hashed_equal(plain: str, hashed: str) -> bool:
    return _password_hasher.verify(plain, hashed)
