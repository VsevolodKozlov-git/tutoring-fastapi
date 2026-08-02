from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

    
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

movie_id_max = 3



@app.get('/')
async def home():
    return {'msg': 'hello world'}


@app.get('/movie/{movie_id}')
async def get_movie_by_id(movie_id: int):
    found = [movie for movie in movies if movie['id']==movie_id]
    if len(found) == 0:
        raise HTTPException(status_code=404, detail='Не найден фильм по id')
    if len(found) > 1:
        raise ValueError('Найдено несколько фильмов по одному id, они не уникальны')
    return found[0]
    

@app.get('/movie')
async def get_movies_all(offset: int = 0, limit: int | None = None, views: int | None = None):
    movies_selected = movies[offset:]
    if limit:
        movies_selected = movies_selected[:limit]
    
    if views:
        movies_selected = [movie for movie in movies if movie['views'] == views]
    
    return movies_selected


class MovieData(BaseModel):
    title: str
    views: int


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