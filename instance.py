# coding: utf-8

# set up the Flask session cookies
SECRET_KEY = 'development_key' # don`t think it seriously

# mail to me if something wrong when the programme is not working in WORK MODE
ADMINEMAIL = ['spacewanderlzx@gmail.com']

# administrators` username and their password
adminsname = [u'admin']
admins = {u'admin': u'1'}
#normal username and their password
usersname = [u'admin',u'spacewander',u'a']
users = {u'admin':u'default', u'spacewander':u'a', u'a':u'a'}

# for SQLAlchemy
Database = 'library.db'

