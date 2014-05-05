# coding: utf-8
from datetime import timedelta, datetime

from flask import session
from sqlalchemy.exc import InvalidRequestError, IntegrityError

from library import app, db
from models.users import User

def set_session_live(is_admin):
    """
    set what time session will live, depend on if the user is an administrator
    """
    if is_admin is True :
        app.permanent_session_lifetime = timedelta(days=1)
    else :
        app.permanent_session_lifetime = timedelta(days=3)

    session.permanent = True

def set_up_users(dic):
    """set up a database with dictionary"""
    db.delete(User)
    for key in dic :
        user = User(username = unicode(key), password = unicode(dic[key]))
        try :
            db.session.add(user)
            db.session.commit()
        except (InvalidRequestError, IntegrityError) :
            pass

def log_error(message):
    """ log the error message in correct format """
    print u"%s %s" % (str(datetime.now() ) , message)


