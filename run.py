#!/bin/env python
# coding: utf-8

from library import set_bugs_logger, set_warning_logger, init_db
from instance import admins, users
from utils import set_up_users
from url import app, db

# run the app
if __name__ == '__main__' :
    if db.get_tables_for_bind() is None :
        init_db(app, db)
    set_up_users(admins)
    set_up_users(users)
    set_bugs_logger()
    set_warning_logger()
    app.run()

