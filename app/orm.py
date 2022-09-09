from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper

import models

"""
ORM module defines SQLAlchemy Table object and maps it to User model
"""

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('tg_id', Integer, index=True),
              Column('first_name', String),
              Column('last_name', String),
              Column('username', String),
              Column('max_score', Integer, index=True)
             )

def start_mapper():
    """
    Function to map User model to Table object
    """
    mapper(models.User, users)
