from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model.user import User
from schemas.user import LoginRequest, UserCreate, UserPublic
from utils.auth import get_hashed_password, get_token, is_hashed_equal
from utils.user import CurrentUser

app = FastAPI()

@app.get('/')
async def home():
    return {'msg': 'hello world'}

movies = [
    {
        'id': 1,
        'title': 'Властелин колец',
        'views': 100
    },
    {
        'id': 2,
        'title': 'Гарри Поттер',
        'views': 80
    },
    {
        'id': 3,
        'title': 'Лицо со шрамом',
        'views': 70
    },
]


@app.get('/movie', status_code=200, summary='Возвращает фильмы')
async def get_movies_all(
    offset: int = 0, limit: int | None = None, views: int | None = None
    ):
    movies_selected = movies[offset:]
    if limit:
        movies_selected = movies_selected[:limit]
    
    if views:
        movies_selected = [movie for movie in movies if movie['views'] == views]
    
    return movies_selected



@app.get('/movie/{movie_id}')
async def get_movie_by_id(movie_id: int):
    movie_list = [movie for movie in movies if movie['id'] == movie_id]
    
    if len(movie_list) == 0:
        raise HTTPException(status_code=404, detail=f'Фильм с id={movie_id} не найден')

    if len(movie_list) > 1:
        raise ValueError(f'Для id={movie_id} для фильма')
    
    return movie_list[0]


class MovieData(BaseModel):
    title: str
    views: int
    
class MovieDataWithId(MovieData):
    id: int
    
movie_id_max = 3


@app.post('/movie')
async def post_movie(movie_data: MovieData) -> MovieDataWithId:
    global movie_id_max
    movie_id_max += 1
    
    new_movie = {
        'id': movie_id_max,
        'title': movie_data.title,
        'views': movie_data.views
    }
    
    movies.append(new_movie)

    return new_movie


@app.post('/register', status_code=201, summary='Регистрация пользователя')
async def register(user_data: UserCreate) -> UserPublic:
    if User.exists(user_data.username):
        raise HTTPException(status_code=400, detail='Username already exists')

    password_hashed = get_hashed_password(user_data.password)
    user = User.create(
        username=user_data.username,
        password_hashed=password_hashed,
        first_name=user_data.first_name,
        second_name=user_data.second_name,
    )

    return UserPublic(
        username=user.username,
        first_name=user.first_name,
        second_name=user.second_name,
    )


@app.post('/login', summary='Авторизация пользователя')
async def login(credentials: LoginRequest):
    user = User.get_by_username(credentials.username)
    if user is None:
        raise HTTPException(status_code=401, detail='login or password is incorrect')

    if not is_hashed_equal(credentials.password, user.password_hashed):
        raise HTTPException(status_code=401, detail='login or password is incorrect')

    access_token = get_token({'username': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@app.get('/profile', summary='Профиль текущего пользователя')
async def get_profile(current_user: CurrentUser) -> UserPublic:
    return current_user
