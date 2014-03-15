# coding: utf-8

from flask import flash
import re

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
    if len(buydate) != 0 and not re.match('\d\d\d\d-\d\d-\d\d', buydate) :
        flash(u'购买日期格式错误，应该为yyyy-mm-dd')
        return False
    return True

def check_items_in_form(title, category, buydate):
    """check all variables in form"""
    return (check_title_is_existed(title) and \
            check_category_is_valid(category) and \
            check_buydate_is_vaild(buydate))