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
    Args:
        session (SessionDep): The database session dependency.
    Returns:
        list[Client]: A list of all clients in the database.
    Swagger:
        summary: Get all clients
        description: Fetches a list of all clients from the database.
        responses:
          200:
            description: A list of clients retrieved successfully.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Client'
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
        dict: The client data if found.
    Raises:
        HTTPException: If the client with the given ID is not found,
                       raises a 404 HTTP exception with a "Client not found" message.
    Swagger:
        summary: Retrieve a client by ID.
        description: Fetches the details of a client from the database using their unique ID.
        parameters:
          - name: client_id
            in: path
            required: true
            description: The unique identifier of the client.
            schema:
              type: integer
        responses:
          200:
            description: Client data retrieved successfully.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: The unique identifier of the client.
                    name:
                      type: string
                      description: The name of the client.
                    email:
                      type: string
                      description: The email of the client.
          404:
            description: Client not found.
    """

    repository = ClientRepository(session)
    client = repository.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/clients/", response_model=Client, tags=["clients"])
async def create_client(client: Client, session: SessionDep):
    """
    Creates a new client in the database.
    Args:
        client (Client): The client object containing the details of the client to be created.
        session (SessionDep): The database session dependency used to interact with the database.
    Returns:
        Client: The newly created client object.
    Raises:
        HTTPException: If there is an error during the creation process.
    Swagger:
        summary: Create a new client
        description: Adds a new client to the database using the provided client details.
        tags:
            - Clients
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/Client'
        responses:
            200:
                description: Successfully created the client.
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Client'
            400:
                description: Invalid input or error during creation.
    """

    repository = ClientRepository(session)
    return repository.add(client)


@router.put("/clients/{client_id}", response_model=Client, tags=["clients"])
async def update_client(client_id: int, client: Client, session: SessionDep):
    """
    Updates an existing client in the database.
    Args:
        client_id (int): The unique identifier of the client to be updated.
        client (Client): The updated client data.
        session (SessionDep): The database session dependency.
    Returns:
        Client: The updated client object.
    Raises:
        HTTPException: If the client with the given ID is not found, raises a 404 error.
    Swagger:
        summary: Update a client.
        description: Updates the details of an existing client in the database.
        parameters:
          - name: client_id
            in: path
            required: true
            description: The unique identifier of the client to update.
            schema:
              type: integer
          - name: client
            in: body
            required: true
            description: The updated client data.
            schema:
              $ref: '#/components/schemas/Client'
        responses:
          200:
            description: Client successfully updated.
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Client'
          404:
            description: Client not found.
    """

    repository = ClientRepository(session)
    updated_client = repository.update(client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client


@router.delete("/clients/{client_id}", response_model=dict, tags=["clients"])
async def delete_client(client_id: int, session: SessionDep):
    """
    Deletes a client by their unique identifier.
    Args:
        client_id (int): The unique identifier of the client to be deleted.
        session (SessionDep): The database session dependency.
    Returns:
        dict: A dictionary containing a success message upon successful deletion.
    Raises:
        HTTPException: If the client with the given ID is not found, raises a 404 error.
    Swagger:
        - summary: Delete a client
        - description: Deletes a client from the database using their unique identifier.
        - parameters:
            - name: client_id
              in: path
              required: true
              description: The unique identifier of the client to delete.
              schema:
                type: integer
        - responses:
            200:
                description: Client deleted successfully.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
                                    example: Client deleted successfully
            404:
                description: Client not found.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                detail:
                                    type: string
                                    example: Client not found
    """

    repository = ClientRepository(session)
    try:
        repository.delete(client_id)
        return {"message": "Client deleted successfully"}
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Client not found")
