from fastapi import APIRouter, HTTPException

from base.db_connection import SessionDep
from movie_rents.models import MovieRentRetrieve, MovieRentCreate, MovieRentUpdate
from movie_rents.repositories import MovieRentRepository
from sqlalchemy.orm.exc import UnmappedInstanceError

router = APIRouter()


@router.get("/movie_rents", tags=["movie_rents"])
async def list_movie_rents(session: SessionDep):
    """
    List all movie rents.
    This asynchronous endpoint retrieves a list of all movie rents from the database.
    Args:
        session (SessionDep): The database session dependency used to interact with the database.
    Returns:
        List[MovieRent]: A list of movie rent objects.
    Raises:
        HTTPException: If there is an issue retrieving the movie rents.
    Swagger:
        - summary: Retrieve all movie rents
        - description: Fetches a list of all movie rents stored in the database.
        - responses:
            200:
                description: A list of movie rents successfully retrieved.
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: '#/components/schemas/MovieRent'
            500:
                description: Internal server error.
    """

    repo = MovieRentRepository(session)
    return repo.get_all()


@router.get("/movie_rents/{id}", tags=["movie_rents"], response_model=MovieRentRetrieve)
async def retrieve_movie_rent(id: int, session: SessionDep):
    """
    Retrieve a movie rent by its ID.
    Args:
        id (int): The unique identifier of the movie rent to retrieve.
        session (SessionDep): The database session dependency.
    Returns:
        dict: The movie rent details if found.
    Raises:
        HTTPException: If the movie rent with the given ID is not found,
                       a 404 status code is returned with an appropriate error message.
    Swagger:
        summary: Retrieve a specific movie rent.
        description: Fetches the details of a movie rent by its unique ID from the database.
        parameters:
          - name: id
            in: path
            required: true
            description: The unique identifier of the movie rent.
            schema:
              type: integer
        responses:
          200:
            description: Movie rent details retrieved successfully.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: The unique identifier of the movie rent.
                    movie_id:
                      type: integer
                      description: The ID of the rented movie.
                    user_id:
                      type: integer
                      description: The ID of the user who rented the movie.
                    rent_date:
                      type: string
                      format: date-time
                      description: The date and time when the movie was rented.
                    return_date:
                      type: string
                      format: date-time
                      description: The date and time when the movie was returned (if applicable).
          404:
            description: Movie rent not found.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    detail:
                      type: string
                      description: Error message indicating the movie rent was not found.
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
        id (int): The ID of the movie rent genre to delete.
        session (SessionDep): The database session dependency.
    Returns:
        bool: True if the deletion was successful, False otherwise.
    Raises:
        HTTPException: If the movie rent genre with the given ID is not found.
    Swagger:
        summary: Delete a movie rent genre
        description: Deletes a movie rent genre from the database using its ID.
        parameters:
          - name: id
            in: path
            required: true
            description: The ID of the movie rent genre to delete.
            schema:
              type: integer
        responses:
          200:
            description: Genre successfully deleted.
            content:
              application/json:
                schema:
                  type: boolean
                  example: true
          404:
            description: Movie Rent not found.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    detail:
                      type: string
                      example: "Movie Rent not found"
    """

    try:
        repo = MovieRentRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie Rent not found")


@router.post("/movie_rents", tags=["movie_rents"], response_model=MovieRentRetrieve)
async def add_movie_rent(movie_rent: MovieRentCreate, session: SessionDep):
    """
    Adds a new movie rent to the system.
    This endpoint allows the creation of a new movie rent record in the database.
    Args:
        movie_rent (MovieRentCreate): The data required to create a new movie rent, including details such as movie ID, user ID, and rental period.
        session (SessionDep): The database session dependency used to interact with the database.
    Returns:
        dict: A dictionary containing the details of the newly created movie rent.
    Raises:
        HTTPException: If there is an issue with the input data or database operation.
    Swagger:
        - summary: Add a new movie rent
        - description: Create a new movie rent record in the system.
        - requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/MovieRentCreate'
        - responses:
            200:
              description: Movie rent successfully created.
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: The ID of the newly created movie rent.
                      movie_id:
                        type: integer
                        description: The ID of the rented movie.
                      user_id:
                        type: integer
                        description: The ID of the user who rented the movie.
                      rental_period:
                        type: string
                        description: The rental period for the movie.
            400:
              description: Invalid input data.
            500:
              description: Internal server error.
    """

    repo = MovieRentRepository(session)
    return repo.add_rent(movie_rent)


@router.put("/movie_rents/{id}", tags=["movie_rents"], response_model=MovieRentRetrieve)
async def update_movie_rent(id: int, movie_rent: MovieRentUpdate, session: SessionDep):
    """
    Updates an existing movie rent record.
    This endpoint allows updating the details of a movie rent record by its ID.
    If the record is not found, a 404 error is returned.
    Args:
        id (int): The unique identifier of the movie rent record to update.
        movie_rent (MovieRentUpdate): The data to update the movie rent record with.
        session (SessionDep): The database session dependency.
    Returns:
        dict: The updated movie rent record.
    Raises:
        HTTPException: If the movie rent record is not found, raises a 404 error.
    Swagger:
        - summary: Update a movie rent record
        - description: Update the details of a movie rent record by its ID.
        - parameters:
            - name: id
              in: path
              required: true
              description: The unique identifier of the movie rent record.
              schema:
                type: integer
            - name: movie_rent
              in: body
              required: true
              description: The data to update the movie rent record with.
              schema:
                $ref: '#/components/schemas/MovieRentUpdate'
        - responses:
            200:
              description: The updated movie rent record.
              content:
                application/json:
                  schema:
                    type: object
            404:
              description: Movie Rent not found.
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
    This endpoint is used to mark a movie rent as closed in the system.
    If the specified movie rent ID does not exist, a 404 error is returned.
    Args:
        id (int): The unique identifier of the movie rent to be closed.
        session (SessionDep): The database session dependency for interacting with the database.
    Returns:
        dict: A dictionary containing the details of the closed movie rent.
    Raises:
        HTTPException: If the movie rent with the given ID is not found,
                       an HTTP 404 error is raised with a "Movie Rent not found" message.
    """

    try:
        repo = MovieRentRepository(session)
        return repo.close_rent(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Movie Rent not found")
