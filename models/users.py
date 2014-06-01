# coding: utf-8

import base64

from library import db
from check import encrypt_password

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    user_id = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self._user_id = self.generalize_user_id(id, username)
        self.password = unicode(encrypt_password(password), errors = 'replace')

    def __repr__(self):
        return '<User %s , user_id %s >' % ( self.username, self.user_id)

    __unicode__ = __str__ = __repr__

    @property
    def user_id(self):
        """ user_id is a readonly property"""
        return self._user_id

    def generalize_user_id(self, id, username):
        """ generalize user id woth id and username """
        return (base64.b64encode(str(id) + username))[:8] # not too long

    def defer_return(self, books=[]):
        """
        defer the deadline for returning book

        books [Entries] reborrow those books
        """
        for book in book :
            book.reborrow()

