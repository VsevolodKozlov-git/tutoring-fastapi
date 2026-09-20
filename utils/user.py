from typing import Annotated

from fastapi import Depends, HTTPException

from model.user import User
from schemas.user import UserPublic
from utils.auth import decode_token


def get_user(token_data: Annotated[dict, Depends(decode_token)]) -> UserPublic:
    username = token_data.get('username')
    if username is None:
        raise HTTPException(status_code=401, detail='Invalid token payload')

    user = User.get_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')

    return UserPublic(
        username=user.username,
        first_name=user.first_name,
        second_name=user.second_name,
    )


CurrentUser = Annotated[UserPublic, Depends(get_user)]
