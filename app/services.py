import unit_of_work
import models

"""
Service layer, uses Unit of Work and model to work with persistent storage - data base.
"""

def get_user(tg_id, uow=unit_of_work.SqlAlchemyUnitOfWork):
    """
    Returns tg_id and max_score of telegram user.
    """
    with uow() as u:
        user = u.users.get(tg_id)
        #if user exist - return only data needed at the moment, overvice - None
        if user:
            return {'tg_id': user.tg_id, 'max_score': user.max_score}

def add_user(tg_id, first_name, last_name, user_name, max_score, uow=unit_of_work.SqlAlchemyUnitOfWork):
    """
    Adds new user to persistent storage
    """
    with uow() as u:
        user = models.User(tg_id, first_name, last_name, user_name, max_score)
        u.users.add(user)
        u.commit()
        return {'tg_id': user.tg_id, 'max_score': user.max_score}

def set_max_score(tg_id, max_score, uow=unit_of_work.SqlAlchemyUnitOfWork):
    """
    Updates max_score of the user
    """
    with uow() as u:
        user = u.users.get(tg_id)
        user.max_score = max_score
        u.commit()

def get_users_list(uow=unit_of_work.SqlAlchemyUnitOfWork):
    """
    List of all users
    """
    with uow() as u:
        users = u.users.list()
        return [{'tg_id': user.tg_id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username, 'max_score': user.max_score} for user in users]
