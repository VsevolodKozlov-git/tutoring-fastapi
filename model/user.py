from schemas.user import UserStored


class User:
    _users: list[dict] = []

    @classmethod
    def get_by_username(cls, username: str) -> UserStored | None:
        for user in cls._users:
            if user['username'] == username:
                return UserStored.model_validate(user)
        return None

    @classmethod
    def exists(cls, username: str) -> bool:
        return any(user['username'] == username for user in cls._users)

    @classmethod
    def create(
        cls,
        username: str,
        password_hashed: str,
        first_name: str,
        second_name: str,
    ) -> UserStored:
        user = {
            'username': username,
            'password_hashed': password_hashed,
            'first_name': first_name,
            'second_name': second_name,
        }
        cls._users.append(user)
        return UserStored.model_validate(user)
