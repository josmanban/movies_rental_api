from fastapi import APIRouter, HTTPException

from base.db_connection import SessionDep
from movie_rents.models import MovieRentRetrieve, MovieRentCreate, MovieRentUpdate
from movie_rents.repositories import MovieRentRepository
from sqlalchemy.orm.exc import UnmappedInstanceError

router = APIRouter()


@router.get("/movie_rents", tags=["movie_rents"])
async def list_movie_rents(session: SessionDep):
    """
    Retrieve a list of all movie rentals.
    This asynchronous function interacts with the MovieRentRepository to fetch
    all movie rental records from the database.
    Args:
        session (SessionDep): The database session dependency used to interact
                              with the database.
    Returns:
        List[MovieRent]: A list of all movie rental records.
    """

    repo = MovieRentRepository(session)
    return repo.get_all()


@router.get("/movie_rents/{id}", tags=["movie_rents"], response_model=MovieRentRetrieve)
async def retrieve_movie_rent(id: int, session: SessionDep):
    """
    Retrieve a movie rent record by its ID.
    Args:
        id (int): The unique identifier of the movie rent record to retrieve.
        session (SessionDep): The database session dependency used to interact with the database.
    Returns:
        MovieRent: The movie rent record corresponding to the given ID.
    Raises:
        HTTPException: If no movie rent record is found with the given ID, a 404 error is raised.
    """

    repo = MovieRentRepository(session)
    instance = repo.get(id)
    if not instance:
        raise HTTPException(status_code=404, detail="Movie Rent not found")
    return instance


@router.delete("/movie_rents/{id}", tags=["movie_rents"])
async def delete_genre(id: int, session: SessionDep):
    """
    Deletes a movie rent genre by its ID.
    Args:
        id (int): The ID of the genre to be deleted.
        session (SessionDep): The database session dependency.
    Returns:
        Any: The result of the deletion operation.
    Raises:
        HTTPException: If the genre with the specified ID is not found,
                       a 404 HTTP exception is raised with an appropriate error message.
    """

    try:
        repo = MovieRentRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie Rent not found")


@router.post("/movie_rents", tags=["movie_rents"], response_model=MovieRentRetrieve)
async def add_movie_rent(movie_rent: MovieRentCreate, session: SessionDep):
    """
    Adds a new movie rent record to the database.
    This asynchronous function handles the creation of a new movie rent entry
    by utilizing the `MovieRentRepository` to persist the data.
    Args:
        movie_rent (MovieRentCreate): The data required to create a new movie rent.
        session (SessionDep): The database session dependency used for database operations.
    Returns:
        The newly created movie rent record as returned by the repository.
    """

    repo = MovieRentRepository(session)
    return repo.add_rent(movie_rent)


@router.put("/movie_rents/{id}", tags=["movie_rents"], response_model=MovieRentRetrieve)
async def update_movie_rent(id: int, movie_rent: MovieRentUpdate, session: SessionDep):
    """
    Update an existing movie rent record.
    Args:
        id (int): The ID of the movie rent record to update.
        movie_rent (MovieRentUpdate): The data to update the movie rent record with.
        session (SessionDep): The database session dependency.
    Returns:
        The updated movie rent record.
    Raises:
        HTTPException: If the movie rent record with the given ID is not found,
                       a 404 HTTP exception is raised with the message "Movie Rent not found".
    """

    try:
        repo = MovieRentRepository(session)
        return repo.update_rent(id, movie_rent)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie Rent not found")


@router.put("/movie_rents/{id}/close", tags=["movie_rents"])
async def close_movie_rent(id: int, session: SessionDep):
    """
    Closes an active movie rent by its ID.
    This asynchronous function attempts to close a movie rent record in the database
    using the provided ID. If the record is not found, an HTTP 404 exception is raised.
    Args:
        id (int): The unique identifier of the movie rent to be closed.
        session (SessionDep): The database session dependency used to interact with the database.
    Returns:
        The result of the `close_rent` method from the `MovieRentRepository`, which
        typically indicates the successful closure of the movie rent.
    Raises:
        HTTPException: If the movie rent with the given ID is not found, a 404 error is raised.
    """

    try:
        repo = MovieRentRepository(session)
        return repo.close_rent(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie Rent not found")
