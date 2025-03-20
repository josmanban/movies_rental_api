from sqlmodel import Field, SQLModel
from fastapi import APIRouter


router = APIRouter()


class ClientBase(SQLModel):
    first_name: str
    last_name: str
    address: str
    license_number: int


class Client(ClientBase, table=True):
    id: int = Field(primary_key=True)
