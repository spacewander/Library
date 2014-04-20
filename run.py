#!/bin/env python
# coding: utf-8

from library import set_bugs_logger, set_warning_logger, app, \
        ADMINPASSWORD, PASSWORD
from utils import set_up_users

# run the app
if __name__ == '__main__' :
    set_up_users(ADMINPASSWORD)
    set_up_users(PASSWORD)
    set_bugs_logger()
    set_warning_logger()
    app.run()

