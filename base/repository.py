from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from base.db_connection import SessionDep

# Declare type variable
T = TypeVar("T")
U = TypeVar("U")


class Repository(Generic[T], ABC):
    """
    Abstract base class for a generic repository pattern.
    This class defines the basic CRUD operations (Create, Read, Update, Delete)
    that any repository implementation should provide. It is designed to work
    with a specific type `T` and requires a session dependency for database
    operations.
    """

    def __init__(self, session: SessionDep):
        self.session = session
        super().__init__()

    @abstractmethod
    def get(self, id: int) -> T:
        """
        Retrieve an object by its unique identifier.
        Args:
            id (int): The unique identifier of the object to retrieve.
        Returns:
            T: The object corresponding to the given identifier.
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """

        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        """
        Retrieve all records from the repository.
        Returns:
            list[T]: A list of all records of type T stored in the repository.
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """

        raise NotImplementedError

    @abstractmethod
    def add(self, new_instance: T) -> T:
        """
        Adds a new instance to the repository.
        Args:
            new_instance (T): The instance to be added.
        Returns:
            T: The added instance.
        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, id: int, instance: T) -> T:
        """
        Update an existing record in the repository with the given instance.
        Args:
            id (int): The unique identifier of the record to update.
            instance (T): The updated instance of the record.
        Returns:
            T: The updated instance of the record.
        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int) -> bool:
        """
        Deletes a record from the repository based on the given ID.
        Args:
            id (int): The unique identifier of the record to be deleted.
        Returns:
            bool: True if the deletion was successful, False otherwise.
        Raises:
            NotImplementedError: If the method is not implemented.
        """

        raise NotImplementedError
