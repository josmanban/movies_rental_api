from sqlmodel import Field, SQLModel, Relationship
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
    copies: list["MovieCopy"] = Relationship(back_populates="movie")


class MovieCreate(BaseMovie):
    stock: int


class MovieUpdate(BaseMovie):
    stock: int


class MoviePublic(BaseMovie):
    id: int
    copies: list["MovieCopyPublic"]


class MovieCopyBase(SQLModel):
    movie_id: int = Field(foreign_key="movie.id")
    code: Optional[str] = Field(index=True)


class MovieCopy(MovieCopyBase, table=True):
    id: int = Field(primary_key=True)
    movie: Movie = Relationship(back_populates="copies")
    rents: list["MovieRentDetail"] = Relationship(back_populates="movie_copy")  # type: ignore # noqa


class MovieCopyPublic(MovieCopyBase):
    id: int
    code: Optional[str]
    movie_id: int
    movie: Movie
