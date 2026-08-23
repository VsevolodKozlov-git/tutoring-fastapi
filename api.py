from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    
movie_id_max = 3


@app.post('/movie')
async def post_movie(movie_data: MovieData):
    global movie_id_max
    movie_id_max += 1
    
    new_movie = {
        'id': movie_id_max,
        'title': movie_data.title,
        'views': movie_data.views
    }
    
    movies.append(new_movie)
    
    return new_movie