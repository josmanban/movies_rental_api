from fastapi import APIRouter, HTTPException

from base.db_connection import SessionDep
from clients.models import Client
from clients.repositories import ClientRepository
from sqlalchemy.orm.exc import UnmappedInstanceError


router = APIRouter()


@router.get("/clients/", response_model=list[Client])
async def get_clients(session: SessionDep):
    repository = ClientRepository(session)
    return repository.get_all()


@router.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: int, session: SessionDep):
    repository = ClientRepository(session)
    client = repository.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/clients/", response_model=Client)
async def create_client(client: Client, session: SessionDep):
    repository = ClientRepository(session)
    return repository.add(client)


@router.put("/clients/{client_id}", response_model=Client)
async def update_client(client_id: int, client: Client, session: SessionDep):
    repository = ClientRepository(session)
    updated_client = repository.update(client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client


@router.delete("/clients/{client_id}", response_model=dict)
async def delete_client(client_id: int, session: SessionDep):
    repository = ClientRepository(session)
    try:
        repository.delete(client_id)
        return {"message": "Client deleted successfully"}
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="Client not found")
