from flask.testing import FlaskClient

from src.models import Movie, db
from tests.utils import create_movie, refresh_db

def test_get_all_movies(test_app: FlaskClient):
    refresh_db()
    
    test_movie = create_movie()
    

    res = test_app.get('/movies')
    page_data: str = res.data.decode()
    
    assert res.status_code == 200
    assert f'<td><a href="/movies/{test_movie.movie_id}">The Dark Knight</a></td>' in page_data
    assert f'<td>Christopher Nolan</td>' in page_data
    assert f'<td>5</td>' in page_data
    
def test_get_all_movies_empty(test_app: FlaskClient):
    refresh_db()
    
    res = test_app.get('/movies')
    page_data: str = res.data.decode()
    
    assert res.status_code == 200
    assert '<td>' not in page_data
    
def test_get_single_movie(test_app: FlaskClient):
    refresh_db()
    
    test_movie = create_movie(rating=4)
    
    res = test_app.get(f'/movies/{test_movie.movie_id}')
    page_data: str = res.data.decode()
    
    assert res.status_code == 200
    assert '<h1>The Dark Knight - 4</h1>' in page_data
    assert '<h2>Christopher Nolan</h2>' in page_data
    
def test_get_single_movie_404(test_app: FlaskClient):
    refresh_db
    
    res = test_app.get('/movies/1')


    assert res.status_code == 404
    
    
def test_create_movie(test_app: FlaskClient):
    refresh_db
    
    res = test_app.post('/movies', data={
        'title': 'The Dark Knight',
        'director': 'Christopher Nolan',
        'rating': '5'
    }, follow_redirects=True)
    page_data = res.data.decode()
    
    assert res.status_code == 200
    assert '<h1>The Dark Knight - 5</h1>' in page_data
    assert '<h2>Christopher Nolan</h2>' in page_data
    
    
def test_create_movie_400(test_app: FlaskClient):
    refresh_db
    
    res = test_app.post('/movies', data={}, follow_redirects=True)
    
    assert res.status_code == 400