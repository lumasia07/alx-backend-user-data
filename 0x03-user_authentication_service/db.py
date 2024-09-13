#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: dict) -> User:
        """Finds a user by arbitrary keyword arguments.

        Args:
            **kwargs (dict): Keyword arguments to filter the query.

        Returns:
            User: The User object matching the query.

        Raises:
            NoResultFound: If no user matches the query.
            InvalidRequestError: If the query arguments are invalid.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the provided arguments")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")

    # def update_user(self, user_id: int, **kwargs: dict) -> None:
    #     """Updates user attributes using the user ID.

    #     Args:
    #         user_id (int): The ID of the user to update.
    #         **kwargs: Attributes to update with their new values.

    #     Raises:
    #         NoResultFound: If no user is found with the given ID.
    #         ValueError: If an invalid attribute is provided.
    #     """
    #     try:
    #         user = self.find_user_by(id=user_id)
    #     except NoResultFound:
    #         raise NoResultFound(f"No user found with ID {user_id}")

    #     for key, value in kwargs.items():
    #         if hasattr(user, key):
    #             setattr(user, key, value)
    #         else:
    #             raise ValueError(f"Attribute {key} is not valid")

    #     self._session.commit()
