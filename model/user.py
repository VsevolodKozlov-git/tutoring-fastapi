from schemas.user import UserStored


class User:
    def __init__(self) -> None:
        self._users: list[dict] = []

    def get_by_username(self, username: str) -> UserStored | None:
        for user in self._users:
            if user['username'] == username:
                return UserStored.model_validate(user)
        return None

    def exists(self, username: str) -> bool:
        return any(user['username'] == username for user in self._users)

    def create(
        self,
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
        self._users.append(user)
        return UserStored.model_validate(user)


user = User()
