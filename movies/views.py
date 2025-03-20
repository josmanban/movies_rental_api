from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm.exc import UnmappedInstanceError

from base.db_connection import SessionDep
from movies.models import Movie, Genre, MovieCreate, MovieUpdate, MoviePublic
from movies.repositories import GenreRepository, MovieRepository

router = APIRouter()


@router.get("/genres", tags=["genres"])
async def list_genres(session: SessionDep):
    """
    Retrieve a list of all movie genres.
    This asynchronous function interacts with the GenreRepository to fetch
    all available genres from the database.
    Args:
        session (SessionDep): The database session dependency used to interact
                              with the database.
    Returns:
        List[Genre]: A list of all genres retrieved from the database.
    """

    repo = GenreRepository(session)
    return repo.get_all()


@router.get("/genres/{id}", tags=["genres"])
async def retrieve_genre(id: int, session: SessionDep):
    """
    Retrieve a genre by its ID.
    Args:
        id (int): The unique identifier of the genre to retrieve.
        session (SessionDep): The database session dependency.
    Returns:
        Genre: The genre instance corresponding to the given ID.
    Raises:
        HTTPException: If the genre with the specified ID is not found,
                       an HTTP 404 exception is raised with a "Genre not found" message.
    """

    repo = GenreRepository(session)
    instance = repo.get(id)
    if not instance:
        raise HTTPException(status_code=404, detail="Genre not found")
    return instance


@router.delete("/genres/{id}", tags=["genres"])
async def delete_genre(id: int, session: SessionDep):
    """
    Deletes a genre by its ID.
    Args:
        id (int): The ID of the genre to delete.
        session (SessionDep): The database session dependency.
    Returns:
        Any: The result of the deletion operation.
    Raises:
        HTTPException: If the genre with the specified ID is not found,
                       a 404 HTTP exception is raised with the message "Genre not found".
    """

    try:
        repo = GenreRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Genre not found")


@router.post("/genres", tags=["genres"])
async def add_genre(genre: Genre, session: SessionDep):
    """
    Asynchronously adds a new genre to the database.
    Args:
        genre (Genre): The genre object to be added.
        session (SessionDep): The database session dependency used for database operations.
    Returns:
        Genre: The newly added genre object.
    Raises:
        Exception: If there is an issue during the database operation.
    """

    repo = GenreRepository(session)
    return repo.add(genre)


@router.post("/genres/{id}", tags=["genres"])
async def update_genre(id: int, genre: Genre, session: SessionDep):
    """
    Updates an existing genre in the database.
    Args:
        id (int): The ID of the genre to update.
        genre (Genre): The updated genre data.
        session (SessionDep): The database session dependency.
    Returns:
        The updated genre object.
    Raises:
        HTTPException: If the genre with the specified ID is not found,
                       raises a 404 HTTP exception with the message "Genre not found".
    """

    try:
        repo = GenreRepository(session)
        return repo.update(id, genre)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Genre not found")


@router.get("/movies", tags=["movies"], response_model=list[MoviePublic])
async def list_movies(session: SessionDep, title: Optional[str] = None):
    """
    Retrieve a list of movies, optionally filtered by title.
    Args:
        session (SessionDep): The database session dependency used to interact with the database.
        title (Optional[str]): An optional string to filter movies by title. If None, all movies are retrieved.
    Returns:
        List[Movie]: A list of movies matching the filter criteria, or all movies if no filter is provided.
    """

    repo = MovieRepository(session)
    return repo.get_all(title=title)


@router.get("/movies/{id}", tags=["movies"], response_model=MoviePublic)
async def retrieve_movie(id: int, session: SessionDep):
    """
    Retrieve a movie by its ID.
    Args:
        id (int): The unique identifier of the movie to retrieve.
        session (SessionDep): The database session dependency.
    Returns:
        Movie: The movie instance if found.
    Raises:
        HTTPException: If the movie with the given ID is not found,
                       raises a 404 HTTP exception with the message "Movie not found".
    """

    repo = MovieRepository(session)
    instance = repo.get(id)
    if not instance:
        raise HTTPException(status_code=404, detail="Movie not found")
    return instance


@router.delete("/movies/{id}", tags=["movies"])
async def delete_movie(id: int, session: SessionDep):
    """
    Deletes a movie from the database by its ID.
    Args:
        id (int): The ID of the movie to be deleted.
        session (SessionDep): The database session dependency.
    Returns:
        bool: True if the movie was successfully deleted, False otherwise.
    Raises:
        HTTPException: If the movie with the given ID is not found, raises a 404 error with the message "Movie not found".
    """

    try:
        repo = MovieRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie not found")


@router.post("/movie", tags=["movies"])
async def add_movie(movie: Movie, session: SessionDep):
    """
    Adds a new movie to the database.
    Args:
        movie (Movie): The movie object containing details of the movie to be added.
        session (SessionDep): The database session dependency used for database operations.
    Returns:
        Movie: The newly added movie object.
    Raises:
        Exception: If there is an error during the database operation.
    """

    repo = MovieRepository(session)
    return repo.add(movie)


@router.post("/movies/with_stock", tags=["movies"], response_model=MoviePublic)
async def add_movie_with_stock(movie: MovieCreate, session: SessionDep):
    """
    Adds a new movie along with its stock information.
    This asynchronous function allows the creation of a new movie entry in the database
    and associates it with stock details. It utilizes the `MovieRepository` to handle
    the database operations.
    Args:
        movie (MovieCreate): The movie data to be added, including title, description,
            release year, and other relevant details.
        session (SessionDep): The database session dependency used to interact with
            the database.
    Returns:
        dict: A dictionary containing the details of the newly created movie along
            with its stock information.
    Raises:
        HTTPException: If there is an issue with the database operation or if the
            movie data is invalid.
    Swagger:
        - summary: Add a new movie with stock.
        - description: Create a new movie entry in the database and associate it with stock details.
        - tags:
            - Movies
        - requestBody:
            required: true
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/MovieCreate'
        - responses:
            200:
                description: Movie successfully created with stock details.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                id:
                                    type: integer
                                    description: The ID of the created movie.
                                title:
                                    type: string
                                    description: The title of the movie.
                                stock:
                                    type: integer
                                    description: The stock quantity of the movie.
            400:
                description: Invalid input data.
            500:
                description: Internal server error.
    """

    repo = MovieRepository(session)
    return repo.add_with_stock(movie)


@router.put("/movies/{id}", tags=["movies"])
async def update_movie(id: int, movie: Movie, session: SessionDep):
    """
    Update an existing movie in the database.
    Args:
        id (int): The unique identifier of the movie to update.
        movie (Movie): The updated movie data.
        session (SessionDep): The database session dependency.
    Returns:
        Movie: The updated movie object.
    Raises:
        HTTPException: If the movie with the given ID is not found,
                       an HTTP 404 error is raised.
    """

    try:
        repo = MovieRepository(session)
        return repo.update(id, movie)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie not found")


@router.put("/movies/{id}/with_stock", tags=["movies"], response_model=MoviePublic)
async def update_movie_with_stock(id: int, movie: MovieUpdate, session: SessionDep):
    """
    Updates a movie's details along with its stock information.
    This asynchronous endpoint updates the details of a movie, including its stock,
    based on the provided movie ID. If the movie is not found, a 404 HTTP exception
    is raised.
    Args:
        id (int): The unique identifier of the movie to be updated.
        movie (MovieUpdate): An object containing the updated movie details.
        session (SessionDep): The database session dependency.
    Returns:
        dict: The updated movie details, including stock information.
    Raises:
        HTTPException: If the movie with the given ID is not found (404 status code).
    Swagger:
        - summary: Update a movie with stock information.
        - description: Updates a movie's details and stock in the database.
        - parameters:
            - name: id
              in: path
              required: true
              description: The ID of the movie to update.
              schema:
                type: integer
            - name: body
              in: body
              required: true
              description: The updated movie details.
              schema:
                $ref: '#/definitions/MovieUpdate'
        - responses:
            200:
              description: Movie successfully updated.
              schema:
                type: object
            404:
              description: Movie not found.
    """

    try:
        repo = MovieRepository(session)
        return repo.update_with_stock(id, movie)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie not found")
