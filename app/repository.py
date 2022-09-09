import abc
import models
from sqlalchemy import desc

"""
Ropository pattern  is abstract idea of persistent data storage.
It is used to docouple Model layer and Data layer
"""

class AbstractRepository(abc.ABC):
    """
    Abstract class for repository pattern
    """
    @abc.abstractmethod
    def add(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    """
    Repository class for User model. It realises add, get and list methods.
    Uses session object to perform it's functionality.
    """
    def __init__(self, session):
        self.session = session

    def add(self, user): 
        self.session.add(user)

    def get(self, tg_id):
        return self.session.query(models.User).filter(models.User.tg_id==tg_id).scalar()

    def list(self):
        return self.session.query(models.User).order_by(desc(models.User.max_score)).all()
