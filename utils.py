# coding: utf-8

from flask import session
from datetime import timedelta

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
        user = User(username=key, password=dic[key])
        try :
            db.session.add(user)
            db.session.commit()
        except :
            pass
