# coding: utf-8
import re
import hashlib
import base64

from flask import flash, session

from library import app

def check_title_is_existed(title):
    """should not be empty"""
    if not title :
        flash(u'没有书名！')
        return False
    return True

def check_category_is_valid(category):
    """
    the input should not contains:
    * number
    * whitespace
    * special char like ! @ $ % ^ & * ( ) + -
    """
    if len(category) != 0 and re.match('[\d\s!@#$%^&*()+-]', category) :
        # if category is not empty
        # match whitespace or digit or some special char
        flash(u'分类输入格式有误，不能包含特殊字符！')
        return False
    return True

def check_buydate_is_vaild(buydate):
    """ should be yyyy-mm-dd"""
    if len(buydate) != 0 and not re.match('\d\d\d\d-\d*\d-\d*\d', buydate) :
        flash(u'购买日期格式错误，应该为yyyy-mm-dd')
        return False
    return True

def check_items_in_form(title, category, buydate):
    """check all variables in form"""
    return (check_title_is_existed(title) and \
            check_category_is_valid(category) and \
            check_buydate_is_vaild(buydate))

def check_admin_logged():
    """check if the administrator is logged or not"""
    if not session.get('logged_in') or not session.get('admin_logged_in'):
        return False
    else:
        return True

def encrypt_password(password):
    """encrypt the password"""
    m = hashlib.md5()
    m.update(password)

    if app.config.salt is not None :
        m.update(app.config.salt)

    return m.digest()

def encrypt_book_record(book):
    """ encrypt the info of each book """
    book.ssid = base64.b16encode(str(book.id))
    return book

def decrypt_book_record(book_ssid):
    """ decrypt the info of each book """
    return base64.b16decode(str(book_ssid))

