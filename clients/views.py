from fastapi import APIRouter, HTTPException

from base.db_connection import SessionDep
from clients.models import Client
from clients.repositories import ClientRepository
from sqlalchemy.orm.exc import UnmappedInstanceError


router = APIRouter()


@router.get("/clients/", response_model=list[Client], tags=["clients"])
async def get_clients(session: SessionDep):
    """
    Retrieve a list of all clients.
    This asynchronous function interacts with the client repository to fetch
    all client records from the database.
    Args:
        session (SessionDep): The database session dependency used to interact
            with the database.
    Returns:
        List[Client]: A list of client objects retrieved from the database.
    """

    repository = ClientRepository(session)
    return repository.get_all()


@router.get("/clients/{client_id}", response_model=Client, tags=["clients"])
async def get_client(client_id: int, session: SessionDep):
    """
    Retrieve a client by their ID.
    Args:
        client_id (int): The unique identifier of the client to retrieve.
        session (SessionDep): The database session dependency.
    Returns:
        Client: The client object if found.
    Raises:
        HTTPException: If the client with the given ID is not found, raises a 404 error with the message "Client not found".
    """

    repository = ClientRepository(session)
    client = repository.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/clients/", response_model=Client, tags=["clients"])
async def create_client(client: Client, session: SessionDep):
    """
    Asynchronously creates a new client in the database.
    Args:
        client (Client): The client object containing the details of the client to be created.
        session (SessionDep): The database session dependency used for interacting with the database.
    Returns:
        Client: The newly created client object after being added to the database.
    """

    repository = ClientRepository(session)
    return repository.add(client)


@router.put("/clients/{client_id}", response_model=Client, tags=["clients"])
async def update_client(client_id: int, client: Client, session: SessionDep):
    """
    Updates an existing client in the database.
    Args:
        client_id (int): The unique identifier of the client to be updated.
        client (Client): An object containing the updated client data.
        session (SessionDep): The database session dependency.
    Returns:
        Client: The updated client object.
    Raises:
        HTTPException: If the client with the given ID is not found, raises a 404 error.
    """

    repository = ClientRepository(session)
    updated_client = repository.update(client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client


@router.delete("/clients/{client_id}", response_model=dict, tags=["clients"])
async def delete_client(client_id: int, session: SessionDep):
    """
    Deletes a client from the database.
    Args:
        client_id (int): The unique identifier of the client to be deleted.
        session (SessionDep): The database session dependency.
    Returns:
        dict: A dictionary containing a success message upon successful deletion.
    Raises:
        HTTPException: If the client with the given ID is not found, raises a 404 error with a "Client not found" message.
    """

    repository = ClientRepository(session)
    try:
        repository.delete(client_id)
        return {"message": "Client deleted successfully"}
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Client not found")
