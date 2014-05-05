# coding: utf-8
import os.path
import logging
from logging.handlers import SMTPHandler
from logging import FileHandler, Formatter

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# for debug improvement
from flask_debugtoolbar import DebugToolbarExtension

from instance import SECRET_KEY, Database, ADMINEMAIL

# configuration
# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# protect my app from cross-site request forgery
WTF_CSRF_ENABLED = True

# static files will be kept in cache for a day
SEND_FILE_MAX_AGE_DEFAULT = 86400
# json should be encoded with utf-8
JSON_AS_ASCII = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, Database)

# here create my tiny app
app = Flask(__name__)
# this method will traverse the giving object
# and use name which all capitalized to configure
app.config.from_object(__name__)
# and if LIBRARY_SETTINGS exists , it will overwrrite the configuration above
app.config.from_envvar('LIBRARY_SETTINGS', silent = True)

app.config['SECRET_KEY'] = SECRET_KEY

# get the database reference from SQLAlchemy
db = SQLAlchemy(app)

salt = 'library'
app.config.salt = salt

# enable the debug mode
app.debug = True

# the toolbar will automatically be injected into Jinja templates
# when debug mode is on
toolbar = DebugToolbarExtension(app)
# enable the Jinja template editor
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True

# some loggers here
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

def init_db(app, db):
    """creat all the tables where it is DEBUG mode"""
    if app.config["DEBUG"] :
        db.create_all()

@app.context_processor
def exist_static_file_wrapper():
    global basedir
    def exist_static_file(filename):
        static_file_dir = os.path.join(basedir, 'static')
        static_file = os.path.join(static_file_dir, filename)

        # compare with the no-min file and pick up the newer one
        max_filename = filename.rsplit('-', 1)[0] + '.' + filename.rsplit('.', 1)[1]
        static_max_file = os.path.join(static_file_dir, max_filename)
        return (not os.path.exists(static_max_file)) or \
                os.path.exists(static_file) and \
                os.path.getatime(static_file) > \
                os.path.getatime(static_max_file)
    return dict(exist_static_file=exist_static_file)

