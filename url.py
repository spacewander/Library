# coding: utf-8

from flask import session, request, render_template, \
        redirect, url_for, abort, \
        flash
from flask.ext.wtf import Form
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from datetime import datetime

# import models
from models.entries import Entries
from models.users import User

# here is from our app
from library import app, db, csrf
from check import check_items_in_form, check_title_is_existed, \
        check_admin_logged, encrypt_book_record, decrypt_book_record
from utils import set_session_live, log_error

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

# this area is for custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# this area is for csrf protection
@csrf.error_handler
def csrf_error(reason):
    form = Form()
    error = u'无效的请求！'
    return render_template('login.html', error=error, form=form), 400

# this area is for route
@app.route('/')
@app.route('/entries')
def show_entries():
    """
    show all the entries in the index page
    """
    books = Entries.query.order_by(Entries.title).all()

    if 'adminname' in session and session['adminname'] is not None :
        user = User.query.filter_by(username=session['adminname']).first()
        books = map(encrypt_book_record, books)
        return render_template('show_entries_admin.html', books=books, user=user)
    elif 'username' in session and session['username'] is not None :
        user = User.query.filter_by(username=session['username']).first()
        return render_template('show_entries.html', books=books, user=user)
    else :
        return redirect(url_for('login'))

@app.route('/admin')
def show_entries_admin():
    """
    show all the entries in the index page for administrators
    """
    books = map(encrypt_book_record, Entries.query.order_by(Entries.title).all())
    if 'adminname' in session and session['adminname'] is not None :
        user = User.query.filter_by(username=session['adminname']).first()
        return render_template('show_entries_admin.html', books=books, user=user)
    else :
        return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_entry():
    """
    add entry if admin is logged in
    """
    if not check_admin_logged() :
        abort(403)

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
        abort(403)

    title = request.form['title']
    category = request.form['category']
    buydate = request.form['buydate']
    ssid = decrypt_book_record(request.form['ssid'])

    if not check_items_in_form(title, category, buydate):
        return redirect(url_for('show_entries_admin'))

    edited_entry = Entries.query.filter_by(
            id=ssid, title=title, category=category, \
                    buydate=buydate).first()

    if edited_entry is not None :
        edited_entry.introduction = request.form['introduction']
        if db.session.is_modified(edited_entry) :
            # commit only if something is modified
            try :
                db.session.commit()
            except IntegrityError as e :
                log_error('error when edit:')
                log_error(e.message)
                flash(u'数据库操作失败导致更新失败！请看后台日志')
        flash(u'成功更新条目')

    return redirect(url_for('show_entries_admin'))

@app.route('/delete')
def delete_entry():
    """
    delete entry if admin is logged in
    """
    if not check_admin_logged() :
        abort(403)

    title = request.args.get('title', default='')
    category = request.args.get('category', default='')
    buydate = request.args.get('buydate', default='')
    ssid = decrypt_book_record(request.args.get('ssid'))

    pre_delete_entry = Entries.query.filter_by(
            id=ssid, title=title, category=category, \
                    buydate=buydate).first()

    if pre_delete_entry is not None :
        try :
            db.session.delete(pre_delete_entry)
            db.session.commit()
            flash(u'删除成功')
        except InvalidRequestError as e :
            log_error('error when delete:')
            log_error(e.message)
            #log_error(u'when delete item %s ' % str(pre_delete_entry))
            # DO NOT use the above one for the F UnicodeEncodeError
            log_error(u'when delete item %s ' % pre_delete_entry)
            db.session.flush()
            flash(u'因为数据库操作原因，删除失败')
    else :
        flash(u'删除失败')

    return redirect(url_for('show_entries_admin'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    As this is a tiny private library system,
    it is not need to let strangers to log in or log up.
    So just add your friends in the app.config
    """
    error = None
    form = Form()

    # only support POST
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
                    session['username'] = username
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
            session['adminname'] = username
            session['username'] = username
            flash(u'欢迎！ %s 管理员' % username)
            return redirect(url_for('show_entries_admin'))

    return render_template('login.html', error=error, form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(u'你已经登出')
    return redirect(url_for('login'))

@app.route('/book/<title>')
def get_book_view(title):
    """
    get the view of book according to the title.

    title [string] the title of the relative book
    """
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
    else :
        introduction = selected_entry.introduction

    if introduction is None :
        introduction = ''

    return render_template('bookview.html', title=title, \
            category=category, buydate=buydate, introduction=introduction)

@app.route('/<user_id>/borrow')
def borrow(user_id):
    """
    the view of borrow page. Users can fill the form of borrowing and submit
    it to the administrators. Then the administrator will be noticed to handle
    it.

    username [sting] the username of User
    """
    user = User.query.filter_by(user_id=user_id).first_or_404()

    # make sure the user who will fill the form is the user
    # whose user_id is reponsitive to the URL
    if user.username == session.get('username') or \
            user.username == session.get('adminname') :
        book_ids = request.args.get('book')
        # fill books list
        books = []
        for book_id in book_ids :
            if type(book_id) != type(0) or book_id < 1 :
                abort(404)
            book = Entries.query.filter_by(id=book_id).first_or_404()
            books.append(book)
        return render_template('borrow.html', books=books, user=user)
    else :
        abort(404)

@app.route('/<user_id>/reborrow')
def reborrow(user_id):
    """
    the view of reborrow page. Users can fill the form of reborrowing and submit
    it to the administrators. Then the administrator will be noticed to handle
    it.

    username [sting] the username of User
    """
    user = User.query.filter_by(user_id=user_id).first_or_404()

    # make sure the user who will fill the form is the user
    # whose user_id is reponsitive to the URL
    if user.username == session.get('username') or \
            user.username == session.get('adminname') :
        book_ids = request.args.get('book')
        # fill books list
        books = []
        for book_id in book_ids :
            if type(book_id) != type(0) or book_id < 1 :
                abort(404)
            book = Entries.query.filter_by(id=book_id).first_or_404()
            books.append(book)
        user.defer_return(books)
    else :
        abort(404)


@app.route('/<user_id>/return')
def return_book(user_id):
    """
    the view of return page. Users can fill the form of return book and submit
    it to the administrators. Then the administrator will be noticed to handle
    it.

    username [sting] the username of User
    """
    user = User.query.filter_by(user_id=user_id).first_or_404()

    # make sure the user who will fill the form is the user
    # whose user_id is reponsitive to the URL
    if user.username == session.get('username') or \
            user.username == session.get('adminname') :
        book_ids = request.args.get('book')
        # fill books list
        books = []
        for book_id in book_ids :
            if type(book_id) != type(0) or book_id < 1 :
                abort(404)
            book = Entries.query.filter_by(id=book_id).first_or_404()
            books.append(book)
        return render_template('return.html', books=books, user=user)
    else :
        abort(404)

