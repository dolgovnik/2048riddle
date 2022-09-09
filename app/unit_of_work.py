import abc
import orm
import repository

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config

"""
Unit of Wqork pattern is abstract idea of atomic operations.
It is finally decouples Service layer and Data layer.
"""

#connect to DB, create session factory, map orm tables to model classes, create tables.
ENGINE_STRING = '{0}+{1}://{2}:{3}@{4}:{5}/{6}'.format(config['sqlalchemy']['DIALECT'], config['sqlalchemy']['DRIVER'], config['DB']['USER'], config['DB']['PASSWORD'], config['DB']['HOST'], config['DB']['PORT'], config['DB']['DB'])
ENGINE = create_engine(ENGINE_STRING)
DEFAULT_SESSION_FACTORY = sessionmaker(ENGINE)
orm.start_mapper()
orm.metadata.create_all(ENGINE)

class AbstractUnitOfWork(abc.ABC):
    """
    Abstract class for Unit of Work pattern with context manager
    """

    users: repository.AbstractRepository

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        #rollback when exit from context manager
        self.rollback()

    @abc.abstractmethod
    def commit(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self, user):
        raise NotImplementedError

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """
    Unit of Work class to access User model repository.
    It is realises context manager interface. 
    """

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.users = repository.SqlAlchemyRepository(self.session)
        return self

    def __exit__(self, *args):
        #first - rollback, then close session
        #rollback after successfull commit - it is ok.
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        #commit method are executed externally
        self.session.commit()

    def rollback(self):
        #rollback method is executed via __exit__ method
        self.session.rollback()
