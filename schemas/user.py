from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    second_name: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UserStored(BaseModel):
    username: str
    password_hashed: str
    first_name: str
    second_name: str


class UserPublic(BaseModel):
    username: str
    first_name: str
    second_name: str
