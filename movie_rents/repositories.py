from datetime import datetime
from sqlmodel import select, delete
from base.repository import Repository
from sqlalchemy.orm.exc import UnmappedInstanceError

from movie_rents.models import (
    MovieRent,
    MovieRentCreate,
    MovieRentUpdate,
    MovieRentDetailCreate,
    MovieRentDetail,
)


class MovieRentRepository(Repository[MovieRent]):
    def get(self, id: int):
        return self.session.get(MovieRent, id)

    def get_all(self):
        statement = select(MovieRent)
        results = self.session.exec(statement).all()
        return results

    def add(self, new_instance: MovieRent):
        self.session.add(new_instance)
        self.session.commit()
        self.session.refresh(new_instance)
        return new_instance

    def update(self, id, instance: MovieRent):
        db_instance = self.session.get(MovieRent, id)
        if not db_instance:
            raise UnmappedInstanceError(db_instance)
        instance_data = instance.model_dump(exclude_unset=True)
        db_instance.sqlmodel_update(instance_data)
        self.session.add(db_instance)
        self.session.commit()
        self.session.refresh(db_instance)
        return db_instance

    def delete(self, id):
        instance = self.session.get(MovieRent, id)
        statement = delete(MovieRentDetail).where(MovieRentDetail.movie_rent_id == id)
        self.session.exec(statement)
        self.session.delete(instance)
        self.session.commit()
        return True

    def add_rent(self, new_instance: MovieRentCreate):
        rent_instance = MovieRent.model_validate(new_instance)
        new_rent = self.add(rent_instance)
        details: list[MovieRentDetailCreate] = new_instance.details

        details_to_save = []
        for detail in details:
            detail.movie_rent_id = new_rent.id
            detail_instance = MovieRentDetail.model_validate(detail)
            details_to_save.append(detail_instance)

        self.session.bulk_save_objects(details_to_save)
        self.session.commit()
        self.session.refresh(new_rent)
        return new_rent

    def update_rent(self, id: int, instance: MovieRentUpdate):
        rent_instance = MovieRent.model_validate(instance)
        updated_rent = self.update(id, rent_instance)

        # remove, add, update MovieRentDetails
        details_to_update = instance.details
        details_to_update_ids = [
            detail.id for detail in details_to_update if hasattr(detail, "id")
        ]

        current_details = self.session.exec(
            select(MovieRentDetail).where(MovieRentDetail.movie_rent_id == id)
        ).all()
        current_details_ids = [detail.id for detail in current_details]

        details_to_remove_ids = [
            detail.id
            for detail in current_details
            if detail.id not in details_to_update_ids
        ]

        for detail in details_to_update:
            if hasattr(detail, "id") and detail.id in current_details_ids:
                detail_instance = self.session.get(MovieRentDetail, detail.id)
                if not detail_instance:
                    raise UnmappedInstanceError(detail_instance)
                detail_instance.sqlmodel_update(detail.model_dump(exclude_unset=True))
                self.session.add(detail_instance)
            else:
                detail.movie_rent_id = id
                detail_instance = MovieRentDetail.model_validate(detail)
                self.session.add(detail_instance)

        statement = delete(MovieRentDetail).where(
            MovieRentDetail.id.in_(details_to_remove_ids)  # type: ignore
        )

        self.session.exec(statement)  # type: ignore
        self.session.commit()
        self.session.refresh(updated_rent)

        return updated_rent

    def close_rent(self, id: int):
        movie_rent = self.get(id)
        movie_rent.is_closed = True
        movie_rent.closed_datetime = datetime.now()

        self.session.add(movie_rent)
        self.session.commit()
        self.session.refresh(movie_rent)
        return movie_rent
