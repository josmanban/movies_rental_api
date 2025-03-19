from fastapi import APIRouter, HTTPException

from base.db_connection import SessionDep
from movie_rents.models import MovieRentRetrieve, MovieRentCreate, MovieRentUpdate
from movie_rents.repositories import MovieRentRepository
from sqlalchemy.orm.exc import UnmappedInstanceError

router = APIRouter()


@router.get("/movie_rents", tags=["movie_rents"])
async def list_movie_rents(session: SessionDep):
    repo = MovieRentRepository(session)
    return repo.get_all()


@router.get("/movie_rents/{id}", tags=["movie_rents"], response_model=MovieRentRetrieve)
async def retrieve_movie_rent(id: int, session: SessionDep):
    repo = MovieRentRepository(session)
    instance = repo.get(id)
    if not instance:
        raise HTTPException(status_code=404, detail="Movie Rent not found")
    return instance


@router.delete("/movie_rents/{id}", tags=["movie_rents"])
async def delete_genre(id: int, session: SessionDep):
    try:
        repo = MovieRentRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie Rent not found")


@router.post("/movie_rents", tags=["movie_rents"], response_model=MovieRentCreate)
async def add_movie_rent(movie_rent: MovieRentCreate, session: SessionDep):
    repo = MovieRentRepository(session)
    return repo.add_rent(movie_rent)


@router.put("/movie_rents/{id}", tags=["movie_rents"], response_model=MovieRentUpdate)
async def update_movie_rent(id: int, movie_rent: MovieRentUpdate, session: SessionDep):
    try:
        repo = MovieRentRepository(session)
        return repo.update_rent(id, movie_rent)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie Rent not found")


@router.put("/movie_rents/{id}/close", tags=["movie_rents"])
async def close_movie_rent(id: int, session: SessionDep):
    try:
        repo = MovieRentRepository(session)
        return repo.close_rent(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie Rent not found")
