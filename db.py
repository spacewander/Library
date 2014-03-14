# coding: utf-8

import sqlite3
from contextlib import closing

# here is from our app
from setting import app, SQLSETTINGS

# here is functions work together with the database
def connect_db():
    """
    a handy function to open a connect for test
    """
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """
    a handy function to exec a script for my database
    """
    with closing(connect_db()) as db:
        with app.open_resource(SQLSETTINGS, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def make_dicts(cursor, row):
    """
    return a dict with key is the index of current cursor object
    and value is the corresponding value of database.
    """
    return dict((cursor.description[idx][0], value) \
            for idx, value in enumerate(row))

def query_db(database, query, args=(), one=False):
    cur = database.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def show_db(database, table):
    """show all thing in a table"""
    if database is None or table is None :
        print "nothing to show"
        return

    try :
        print ''
        print "%s :" % table
        cur = database.execute('select * from ' + table)
        for row in cur.fetchall():
            print row
    except sqlite3.OperationalError as e :
        print e

def set_users_with_dict(dic):
    """set up a database with dictionary"""
    db = connect_db()
    try :
        # just for test
        db.execute('select * from users')
    except sqlite3.OperationalError :
        init_db()
    for key in dic:
        db.execute('insert into users (username, password) values (?, ?)', \
                        [key, dic[key]])
        db.commit()

