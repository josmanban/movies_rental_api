from sqlmodel import select
from base.repository import Repository
from sqlalchemy.orm.exc import UnmappedInstanceError

from movies.models import Movie, MovieCreate, MovieUpdate, MovieCopy, Genre


class GenreRepository(Repository[Genre]):
    """
    A repository class for managing CRUD operations on the Genre model.
    Methods:
        get(id: int) -> Genre:
            Retrieves a Genre instance by its ID.
        get_all() -> List[Genre]:
            Retrieves all Genre instances from the database.
        add(new_instance: Genre) -> Genre:
            Adds a new Genre instance to the database, commits the transaction,
            and refreshes the instance.
        update(id: int, instance: Genre) -> Genre:
            Updates an existing Genre instance in the database with the provided data.
        delete(id: int) -> bool:
            Deletes a Genre instance from the database by its ID and commits the transaction.
    """

    def get(self, id: int):
        return self.session.get(Genre, id)

    def get_all(self):
        statement = select(Genre)
        results = self.session.exec(statement).all()
        return results

    def add(self, new_instance: Genre):
        self.session.add(new_instance)
        self.session.commit()
        self.session.refresh(new_instance)
        return new_instance

    def update(self, id, instance: Genre):
        db_instance = self.session.get(Genre, id)
        if not db_instance:
            raise UnmappedInstanceError(db_instance)
        instance_data = instance.model_dump(exclude_unset=True)
        db_instance.sqlmodel_update(instance_data)
        self.session.add(db_instance)
        self.session.commit()
        self.session.refresh(db_instance)
        return db_instance

    def delete(self, id):
        instance = self.session.get(Genre, id)
        self.session.delete(instance)
        self.session.commit()
        return True


class MovieRepository(Repository[Movie]):
    """
    A repository class for managing CRUD operations on the Movie model.
    Methods:
        get(id: int) -> Movie:
            Retrieves a Movie instance by its ID.
        get_all() -> List[Movie]:
            Retrieves all Movie instances from the database.
        add(new_instance: Movie) -> Movie:
            Adds a new Movie instance to the database, commits the transaction,
            and refreshes the instance.
        update(id: int, instance: Movie) -> Movie:
            Updates an existing Movie instance in the database with the provided data.
        delete(id: int) -> bool:
            Deletes a Movie instance from the database by its ID and commits the transaction.
    """

    def get(self, id: int):
        return self.session.get(Genre, id)

    def get_all(self):
        statement = select(Movie)
        results = self.session.exec(statement).all()
        return results

    def add(self, new_instance: Movie):
        self.session.add(new_instance)
        self.session.commit()
        self.session.refresh(new_instance)
        return new_instance

    def update(self, id: int, instance: Movie):
        db_instance = self.session.get(Movie, id)
        if not db_instance:
            raise UnmappedInstanceError(db_instance)
        instance_data = instance.model_dump(exclude_unset=True)
        db_instance.sqlmodel_update(instance_data)
        self.session.add(db_instance)
        self.session.commit()
        self.session.refresh(db_instance)
        return db_instance

    def delete(self, id: int):
        instance = self.session.get(Movie, id)
        self.session.delete(instance)
        self.session.commit()
        return True

    def add_with_stock(self, movie: MovieCreate):
        movie_instance = Movie.model_validate(movie)
        new_movie = self.add(movie_instance)
        stock = movie.stock

        movie_copies = []
        for i in range(stock):
            specific_movie = MovieCopy(movie_id=new_movie.id)
            movie_copies.append(specific_movie)
        self.session.bulk_save_objects(movie_copies)
        self.session.refresh(new_movie)
        self.session.commit()

        return new_movie

    def update_with_stock(self, id: int, movie: MovieUpdate):
        movie_instance = Movie.model_validate(movie)
        updated_movie = self.update(id, movie_instance)

        # reduce or increase the number of movies in stock
        stock = movie.stock
        movie_copies_count = len(
            self.session.exec(select(MovieCopy).where(MovieCopy.movie_id == id)).all()
        )

        if stock > movie_copies_count:
            movie_copies = []
            for i in range(stock - movie_copies_count):
                specific_movie = MovieCopy(movie_id=updated_movie.id)
                movie_copies.append(specific_movie)
            self.session.bulk_save_objects(movie_copies)
        elif stock < movie_copies_count:
            results = self.session.exec(
                select(MovieCopy)
                .where(MovieCopy.movie_id == id)
                .limit(movie_copies_count - stock)
            ).all()
            for movie_copy in results:
                self.session.delete(movie_copy)
        self.session.commit()
        self.session.refresh(updated_movie)
        return updated_movie
