from typing import Annotated

from fastapi import Depends, HTTPException

from model.user import user
from schemas.user import UserPublic
from utils.auth import decode_token


def get_user(token_data: Annotated[dict, Depends(decode_token)]) -> UserPublic:
    username = token_data.get('sub')
    if username is None:
        raise HTTPException(status_code=401, detail='Invalid token payload')

    user_data = user.get_by_username(username)
    if user_data is None:
        raise HTTPException(status_code=401, detail='User not found')

    return UserPublic(
        username=user_data.username,
        first_name=user_data.first_name,
        second_name=user_data.second_name,
    )


CurrentUser = Annotated[UserPublic, Depends(get_user)]
