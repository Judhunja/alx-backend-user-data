#!/usr/bin/env python3
""" This module contains a class db """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import InvalidRequestError


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
        """Adds a new user to the database """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Return first row in the database as filtered by
            the kwargs """
        # Obtain all the columns using c representing column in inspect
        columns = [c.name for c in inspect(User).c]
        for key in kwargs.keys():
            if key not in columns:
                raise InvalidRequestError
        found_user = self._session.query(User).filter_by(**kwargs).first()
        if found_user is None:
            raise NoResultFound
        return found_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user's attributes """
        columns = [c.name for c in inspect(User).c]
        for key in kwargs.keys():
            if key not in columns:
                raise ValueError
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            user.key = value
