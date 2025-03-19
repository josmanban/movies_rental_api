from sqlmodel import Field, SQLModel
from typing import Optional


class Genre(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    description: str


class BaseMovie(SQLModel):
    title: str = Field(index=True)
    description: str
    year: int
    director: str

    genre_id: int = Field(foreign_key="genre.id")


class Movie(BaseMovie, table=True):
    id: int = Field(default=None, primary_key=True)


class MovieCreate(BaseMovie):
    stock: int


class MovieUpdate(BaseMovie):
    stock: int


class MovieCopy(SQLModel, table=True):
    id: int = Field(primary_key=True)
    movie_id: int = Field(foreign_key="movie.id")
    code: Optional[str] = Field(index=True)
