# coding: utf-8

from flask import session, request, render_template, \
        redirect, url_for, abort, \
        flash, g
from flask.ext.wtf import Form
from datetime import datetime, timedelta

# here is from our app
from db import connect_db, set_users_with_dict#, show_db
#from db import init_db
from setting import app, PASSWORD, ADMINPASSWORD, \
        set_bugs_logger, set_warning_logger
from check import check_items_in_form, check_title_is_existed

# this area is for the database operation when request
def get_db():
    if g.db is None :
        g.db = connect_db()

@app.before_request
def before_request():
    """
    call before request
    """
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """
    call after request or when request failed
    """
    if g.db is not None:
        g.db.close()

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
    get_db()
    cur = g.db.execute('select title, category, buydate, introduction from entries \
                                            order by id asc , title asc')
    entries = [dict(title=row[0],category=row[1], buydate=row[2], introduction=row[3]) \
            for row in cur.fetchall()]
    return render_template('show_entries.html', books=entries)

@app.route('/admin')
def show_entries_admin():
    """
    show all the entries in the index page for administrators
    """
    get_db()
    cur = g.db.execute('select title, category, buydate, introduction from entries \
                                            order by id asc , title asc')
    entries = [dict(title=row[0],category=row[1], buydate=row[2], introduction=row[3]) \
            for row in cur.fetchall()]
    return render_template('show_entries_admin.html', books=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    """
    add entry if admin is logged in
    """
    if not session.get('logged_in') :
        abort(401)

    title = request.form['title']
    category = request.form['category']
    buydate = request.form['buydate']

    if not check_items_in_form(title, category, buydate):
        return redirect(url_for('show_entries'))

    get_db()
    g.db.execute('insert into entries (title, category, buydate, introduction) \
                                                        values (?, ?, ?, ?)', \
                        [title, category, buydate, request.form['introduction']])

    g.db.commit()
    flash(u'成功添加新的条目')
    return redirect(url_for('show_entries'))

@app.route('/edit', methods=['POST'])
def edit_entry():
    """
    edit entry if admin is logged in
    """
    if not session.get('logged_in') :
        abort(401)

    title = request.form['title']
    category = request.form['category']
    buydate = request.form['buydate']

    if not check_items_in_form(title, category, buydate):
        return redirect(url_for('show_entries'))

    get_db()
    g.db.execute('update entries set category = ?, buydate = ?, \
                            introduction = ? where title = ?', \
             [category, buydate, request.form['introduction'], title])

    g.db.commit()
    flash(u'成功更新条目')
    return redirect(url_for('show_entries'))

@app.route('/delete')
def delete_entry():
    """
    delete entry if admin is logged in
    """
    if not session.get('logged_in') :
        abort(401)

    title = request.args.get('title', default='')
    category = request.args.get('category', default='')
    buydate = request.args.get('buydate', default='')

    get_db()
    # check if the entry is in the database before we can safely delete it.
    # Maybe wasteful?
    cur = g.db.execute('select * from entries where title = ? and \
                                                        category = ? and \
                                                        buydate = ?', \
                                                [title, category, buydate])

    if cur.fetchall() is not None :
        g.db.execute('delete from entries where title = ? \
                            and category = ? and buydate = ?', \
                            [title, category, buydate])
        g.db.commit()
        flash(u'删除成功')
    else :
        flash(u'删除失败。要删除的项不在数据库中')
    return redirect(url_for('show_entries'))

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

    get_db()
    cur = g.db.execute('select introduction from entries where title = ? and \
                                                        category = ? and \
                                                        buydate = ?', \
                                                [title, category, buydate])

    introduction, = cur.fetchall()[0]
    if introduction is None :
        introduction = ''

    return render_template('bookview.html', title=title, \
            category=category, buydate=buydate, introduction=introduction)

def set_session_live(is_admin):
    """
    set what time session will live, depend on if the user is an administrator
    """
    if is_admin is True :
        app.permanent_session_lifetime = timedelta(days=1)
    else :
        app.permanent_session_lifetime = timedelta(days=3)

    session.permanent = True

# run the app
if __name__ == '__main__' :
    #init_db()
    set_users_with_dict(ADMINPASSWORD)
    set_users_with_dict(PASSWORD)
    set_bugs_logger()
    set_warning_logger()
    app.run()
    #show_db(g.db, 'users')
    #show_db(g.db, 'entries')

