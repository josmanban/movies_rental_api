from sqlmodel import Field, SQLModel


class Client(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    address: str
    license_number: int
