from fastapi import APIRouter, HTTPException

from base.db_connection import SessionDep
from movies.models import Movie, Genre, MovieCreate, MovieUpdate
from movies.repositories import GenreRepository, MovieRepository
from sqlalchemy.orm.exc import UnmappedInstanceError

router = APIRouter()


@router.get("/genres", tags=["genres"])
async def list_genres(session: SessionDep):
    repo = GenreRepository(session)
    return repo.get_all()


@router.get("/genres/{id}", tags=["genres"])
async def retrieve_genre(id: int, session: SessionDep):
    repo = GenreRepository(session)
    instance = repo.get(id)
    if not instance:
        raise HTTPException(status_code=404, detail="Genre not found")
    return instance


@router.delete("/genres/{id}", tags=["genres"])
async def delete_genre(id: int, session: SessionDep):
    try:
        repo = GenreRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Genre not found")


@router.post("/genres", tags=["genres"])
async def add_genre(genre: Genre, session: SessionDep):
    repo = GenreRepository(session)
    return repo.add(genre)


@router.post("/genres/{id}", tags=["genres"])
async def update_genre(id: int, genre: Genre, session: SessionDep):
    try:
        repo = GenreRepository(session)
        return repo.update(id, genre)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Genre not found")


@router.get("/movies", tags=["movies"])
async def list_movies(session: SessionDep):
    repo = MovieRepository(session)
    return repo.get_all()


@router.get("/movies/{id}", tags=["movies"])
async def retrieve_movie(id: int, session: SessionDep):
    repo = MovieRepository(session)
    instance = repo.get(id)
    if not instance:
        raise HTTPException(status_code=404, detail="Movie not found")
    return instance


@router.delete("/movies/{id}", tags=["movies"])
async def delete_movie(id: int, session: SessionDep):
    try:
        repo = MovieRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie not found")


@router.post("/genres", tags=["genres"])
async def add_movie(movie: Movie, session: SessionDep):
    repo = MovieRepository(session)
    return repo.add(movie)


@router.post("/movies/with_stock", tags=["movies"])
async def add_movie_with_stock(movie: MovieCreate, session: SessionDep):
    repo = MovieRepository(session)
    return repo.add_with_stock(movie)


@router.post("/movies/{id}", tags=["movies"])
async def update_movie(id: int, movie: Movie, session: SessionDep):
    try:
        repo = MovieRepository(session)
        return repo.update(id, movie)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie not found")


@router.post("/movies/{id}/with_stock", tags=["movies"])
async def update_movie_with_stock(id: int, movie: MovieUpdate, session: SessionDep):
    try:
        repo = MovieRepository(session)
        return repo.update_with_stock(id, movie)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie not found")
