from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class MovieRentBase(SQLModel):
    client_id: int = Field(foreign_key="client.id")
    creation_datetime: Optional[datetime] = Field(default=datetime.now())
    closed_datetime: Optional[datetime] = Field(default=None)
    is_closed: Optional[bool] = Field(default=False)


class MovieRent(MovieRentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    details: list["MovieRentDetail"] = Relationship(
        back_populates="movie_rent", cascade_delete=True
    )


class MovieRentCreate(MovieRentBase):
    details: list["MovieRentDetail"]


class MovieRentUpdate(MovieRentBase):
    details: list["MovieRentDetail"]


class MovieRentRetrieve(MovieRentBase):
    details: list["MovieRentDetail"]
    id: int


class MovieRentDetailBase(SQLModel):
    movie_id: int = Field(default=None, foreign_key="movie.id")
    movie_rent_id: int = Field(
        default=None, foreign_key="movierent.id", ondelete="CASCADE"
    )


class MovieRentDetail(MovieRentDetailBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie_rent: MovieRent = Relationship(back_populates="details")
