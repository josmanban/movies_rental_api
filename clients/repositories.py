from sqlmodel import select
from base.repository import Repository
from sqlalchemy.orm.exc import UnmappedInstanceError

from clients.models import Client


class ClientRepository(Repository[Client]):
    def get(self, id: int):
        return self.session.get(Client, id)

    def get_all(self):
        statement = select(Client)
        result = self.session.exec(statement).all()
        return result

    def add(self, new_instance: Client) -> Client:
        self.session.add(new_instance)
        self.session.commit()
        self.session.refresh(new_instance)
        return new_instance

    def update(self, id: int, instance: Client) -> Client:
        db_instance = self.session.get(Client, id)
        if not db_instance:
            raise UnmappedInstanceError(db_instance)
        instance_data = instance.model_dump(exclude_unset=True)
        db_instance.sqlmodel_update(instance_data)
        self.session.add(db_instance)
        self.session.commit()
        self.session.refresh(db_instance)
        return db_instance

    def delete(self, id: int) -> bool:
        instance = self.session.get(Client, id)
        self.session.delete(instance)
        self.session.commit()
        return True
