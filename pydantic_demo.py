from typing import Annotated

from pydantic import BaseModel, NonNegativeInt, BeforeValidator, AfterValidator


def non_negative(number):
    if number < 0:
        raise ValueError("Должно быть >= 0")

    return number


def convert_from_dollars(money_str) -> int:
    if money_str[-1] == "$":
        money_str = money_str[:-1]
    return int(money_str)


class MovieData(BaseModel):
    title: str
    # views: int
    # views: NonNegativeInt
    # views: Annotated[int, BeforeValidator(lambda x: x >= 0)]
    # views: Annotated[int, AfterValidator(lambda x: x >= 0)]
    views: Annotated[int, AfterValidator(non_negative)]
    gross: Annotated[int, BeforeValidator(convert_from_dollars)]


def get_sum_of_views(data_list: list[MovieData]):
    result = 0
    for data in data_list:
        result += data.gross
    return result


def conversion_demo():
    d = {"title": "Титаник", "views": 100, "gross": "10$"}
    model = MovieData.model_validate(d)
    print(model)
    d_from_model = model.model_dump()
    print(d_from_model)


if __name__ == "__main__":
    conversion_demo()
    data_list = [
        MovieData(title="Титаник", views=100, gross="10$"),
        MovieData(title="Бойцовский клуб", views=10, gross="5$"),
    ]

    print(get_sum_of_views(data_list))
