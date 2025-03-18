from sqlmodel import Field, SQLModel


class Rent(SQLModel, table=True):
    id: int = Field(primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    is_closed: bool = Field(default=False)


class RentDetail(SQLModel, table=True):
    id: int = Field(primary_key=True)

    movie_id: int = Field(foreign_key="movie.id")
