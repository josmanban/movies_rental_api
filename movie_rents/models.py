from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class MovieRentBase(SQLModel):
    client_id: int = Field(foreign_key="client.id")
    creation_datetime: Optional[datetime] = Field(default=datetime.now())
    closed_datetime: Optional[datetime] = Field(default=None)
    is_closed: Optional[bool] = Field(default=False)


class MovieRent(MovieRentBase, table=True):
    id: int = Field(default=None, primary_key=True)


class MovieRentDetailBase(SQLModel):
    movie_id: int = Field(default=None, foreign_key="movie.id")
    movie_rent_id: int = Field(default=None, foreign_key="movierent.id")


class MovieRentDetail(MovieRentDetailBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MovieRentDetailCreate(MovieRentDetailBase):
    pass


class MovieRentDetailUpdate(MovieRentDetailBase):
    id: Optional[int] = Field(default=None, primary_key=True)


class MovieRentCreate(MovieRentBase):
    details: list[MovieRentDetailCreate]


class MovieRentUpdate(MovieRentBase):
    details: list[MovieRentDetailUpdate]
