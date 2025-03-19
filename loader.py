import json
import datetime
from movies.models import Genre, Movie, MovieCopy
from clients.models import Client
from movie_rents.models import MovieRent, MovieRentDetail
from sqlmodel import Session

from base.db_connection import engine


def load_genres(engine):
    with Session(engine) as session:
        with open("./datasets/genre.json") as f:
            output_data = json.load(f)
            for genre_data in output_data:
                genre = Genre(**genre_data)
                session.add(genre)
            session.commit()


def load_movies(engine):
    with Session(engine) as session:
        with open("./datasets/movie.json") as f:
            output_data = json.load(f)
            for movie_data in output_data:
                movie = Movie(**movie_data)
                session.add(movie)
            session.commit()


def load_movies_copies(engine):
    with Session(engine) as session:
        with open("./datasets/moviecopy.json") as f:
            output_data = json.load(f)
            for movie_copy_data in output_data:
                movie_copy = MovieCopy(**movie_copy_data)
                session.add(movie_copy)
            session.commit()


def load_clients(engine):
    with Session(engine) as session:
        with open("./datasets/client.json") as f:
            output_data = json.load(f)
            for client_data in output_data:
                client = Client(**client_data)
                session.add(client)
            session.commit()


def load_movie_rents(engine):
    with Session(engine) as session:
        with open("./datasets/movierent.json") as f:
            output_data = json.load(f)
            for movie_rent_data in output_data:
                movie_rent = MovieRent(**movie_rent_data)
                movie_rent.creation_datetime = datetime.datetime.fromisoformat(
                    movie_rent_data.get("creation_datetime")
                )
                if movie_rent_data.get("closed_datetime"):
                    movie_rent.closed_datetime = datetime.datetime.fromisoformat(
                        movie_rent_data.get("closed_datetime")
                    )
                session.add(movie_rent)
            session.commit()


def load_movie_rent_details(engine):
    with Session(engine) as session:
        with open("./datasets/movierentdetail.json") as f:
            output_data = json.load(f)
            for movie_rent_detail_data in output_data:
                movie_rent_detail = MovieRentDetail(**movie_rent_detail_data)
                session.add(movie_rent_detail)
            session.commit()


def load_initial_data(engine):
    load_genres(engine)
    load_movies(engine)
    load_movies_copies(engine)
    load_clients(engine)
    load_movie_rents(engine)
    load_movie_rent_details(engine)


def main():
    load_initial_data(engine)


if __name__ == "__main__":
    main()
