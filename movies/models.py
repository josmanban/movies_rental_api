from sqlmodel import Field, SQLModel


class Genre(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    description: str


class Movie(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(index=True)
    description: str
    year: int
    director: str

    genre_id: int = Field(foreign_key="genre.id")


class SpecificMovie(SQLModel, table=True):
    id: int = Field(primary_key=True)
    movie_id: int = Field(foreign_key="movie.id")
