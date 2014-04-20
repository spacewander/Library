# coding: utf-8

from flask import session, request, render_template, \
        redirect, url_for, abort, \
        flash
from flask.ext.wtf import Form
from datetime import datetime

# here is from our app
from library import app, db
from check import check_items_in_form, check_title_is_existed, check_admin_logged
from utils import set_session_live
# import models
from models.entries import Entries

# this area is for the database operation when request

@app.before_request
def before_request():
    """
    call before request
    """
    pass

@app.teardown_request
def teardown_request(exception):
    """
    call after request or when request failed
    """
    if db.session is not None:
        db.session.close()
    else:
        pass

# this area is for the context variable in jinja2
@app.context_processor
def get_today():
    """
    get today's date and show it
    """
    return dict(today = str(datetime.today())[:10])

# this area is for route
@app.route('/')
@app.route('/entries')
def show_entries():
    """
    show all the entries in the index page
    """
    books = Entries.query.order_by(Entries.title).all()
    return render_template('show_entries.html', books=books)

@app.route('/admin')
def show_entries_admin():
    """
    show all the entries in the index page for administrators
    """
    books = Entries.query.order_by(Entries.title).all()
    return render_template('show_entries_admin.html', books=books)

@app.route('/add', methods=['POST'])
def add_entry():
    """
    add entry if admin is logged in
    """
    if not check_admin_logged() :
        abort(401)

    title = request.form['title']
    category = request.form['category']
    buydate = request.form['buydate']
    introduction = request.form['introduction']

    if not check_items_in_form(title, category, buydate):
        return redirect(url_for('show_entries_admin'))

    new_entry = Entries(title, category, buydate, introduction)
    db.session.add(new_entry)

    try :
        db.session.commit()
    except IntegrityError as e :
        flash(e.message)
        return redirect(url_for('show_entries_admin'))

    flash(u'成功添加新的条目')
    return redirect(url_for('show_entries_admin'))

@app.route('/edit', methods=['POST'])
def edit_entry():
    """
    edit entry if admin is logged in
    """
    if not check_admin_logged() :
        abort(401)

    title = request.form['title']
    category = request.form['category']
    buydate = request.form['buydate']

    if not check_items_in_form(title, category, buydate):
        return redirect(url_for('show_entries_admin'))

    # if the entry is not existed in the database, nothing will change. This is not matter.
    # FIXME
    edited_entry = Entries.query.filter_by(title=title, category=category, \
            buydate=buydate).first()

    if edited_entry is not None :
        edited_entry.introduction = request.form['introduction']
        if db.session.is_modified(edited_entry) :
            # commit only if something is modified
            db.session.commit()
        flash(u'成功更新条目')

    return redirect(url_for('show_entries_admin'))

@app.route('/delete')
def delete_entry():
    """
    delete entry if admin is logged in
    """
    if not check_admin_logged() :
        abort(401)

    title = request.args.get('title', default='')
    category = request.args.get('category', default='')
    buydate = request.args.get('buydate', default='')

    pre_delete_entry = Entries(title, category, buydate)

    if pre_delete_entry is not None :
        db.session.delete(pre_delete_entry)
        db.session.commit()
        flash(u'删除成功')
    else :
        flash(u'删除失败')

    return redirect(url_for('show_entries_admin'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    as this is a tiny private library system,
    it is not need to let strangers to log in or log up.
    So just add your friends in the app.config
    """
    error = None
    form = Form()

    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        # if the user is not an administrator
        if username not in app.config['ADMINNAME'] :
            # if the user is a normal user
            if username in app.config['USERNAME'] :
                if password != (app.config['PASSWORD'])[username] :
                    error = 'Invalid password'
                    return render_template('login.html', error=error, form=form)
                else :
                    # log as normal user
                    session['logged_in'] = True
                    flash(u'欢迎！ %s' % username)
                    set_session_live(is_admin=False)
                    return redirect(url_for('show_entries'))
            else :
                error = 'Invalid username' # the user is a stranger
        # check password for administrator
        elif request.form['password'] != (app.config['ADMINPASSWORD'])[username] :
            error = 'Invalid password'
        else :
            # log as administrator
            session['logged_in'] = True
            session['admin_logged_in'] = True
            set_session_live(is_admin=True)
            flash(u'欢迎！ %s 管理员' % username)
            return redirect(url_for('show_entries_admin'))

    return render_template('login.html', error=error, form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(u'你已经登出')
    return redirect(url_for('show_entries'))

@app.route('/book/<title>')
def get_book_view(title):
    # 使用来自数据库的数据来动态生成页面而不是映射到对应的静态页面上去
    # 目前对于这个小应用还可以，在将来可能需要修改
    if not check_title_is_existed(title) :
        return redirect(url_for('show_entries'))

    category = request.args.get('category', default='')
    buydate = request.args.get('buydate', default='')

    selected_entry = Entries.query.filter_by(title=title, category=category, \
            buydate=buydate).first()
    if selected_entry is None :
        flash(u'无法找到对应的项')
        return redirect(url_for('show_entries'))
    else :
        introduction = selected_entry.introduction

    if introduction is None :
        introduction = ''

    return render_template('bookview.html', title=title, \
            category=category, buydate=buydate, introduction=introduction)


