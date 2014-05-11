#!/bin/env python
# coding: utf-8

from library import set_bugs_logger, set_warning_logger, init_db
from instance import admins, users, adminsname, usersname
from utils import set_up_users
from url import app, db

# run the app
if __name__ == '__main__' :
    if db.get_tables_for_bind() is None :
        init_db(app, db)

    # set up some config
    app.config["ADMINNAME"] = adminsname;
    app.config["USERNAME"] = usersname;
    app.config["ADMINPASSWORD"] = admins;
    app.config["PASSWORD"] = users;

    set_up_users(admins)
    set_up_users(users)
    set_bugs_logger()
    set_warning_logger()
    app.run()

