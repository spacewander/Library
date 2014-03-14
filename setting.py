# coding: utf-8

import logging
from logging.handlers import SMTPHandler
from logging import FileHandler, Formatter

from flask import Flask

# configuration
DATABASE = '/tmp/library.db'
DEBUG = True

SECRET_KEY = 'development_key' # don`t think it seriously
# protect my app from cross-site request forgery
WTF_CSRF_ENABLED = True

# static files will be kept in cache for a day
SEND_FILE_MAX_AGE_DEFAULT = 86400
# json should be encoded with utf-8
JSON_AS_ASCII = False

# mail to me if something wrong when the programme is not working in DEBUG MODE
ADMINEMAIL = ['spacewanderlzx@gmail.com']

# administrators` username and their password
ADMINNAME = ['admin']
ADMINPASSWORD = {'admin':'1'}
#normal username and their password
USERNAME = ['admin','spacewander','a']
PASSWORD = {'admin':'default', 'spacewander':'a', 'a':'a'}
SQLSETTINGS = 'schema.sql'

# here create my tiny app
app = Flask(__name__)
# this method will traverse the giving object
# and use name which all capitalized to configure
app.config.from_object(__name__)
# and if LIBRARY_SETTINGS exists , it will overwrrite the configuration above
app.config.from_envvar('LIBRARY_SETTINGS', silent = True)

def set_bugs_logger():
    """set logger for bugs report"""
    if not app.debug :
        mail_handler = SMTPHandler('127.0.0.1', 'server-error@auto.com', \
                                    ADMINEMAIL, 'Library is in trouble')
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter('''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(Module)s
            Function:           %(funcName)s
            Time:               %(asctime)s

            Message:

            %(message)s
            '''))
        app.logger.addHandler(mail_handler)

def set_warning_logger():
    """set logger for warning log"""
    if not app.debug :
        file_handler = FileHandler('Library_bad_news.txt')
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(Formatter( \
                '%(asctime)s %(levelname)s: %(message)s \
                 [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)
