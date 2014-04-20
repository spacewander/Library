# coding: utf-8

import os
import unittest
import tempfile

import library

class LibaryTestCase(unittest.TestCase):

    def __init__(self, *args):
        super(LibaryTestCase, self).__init__(*args)
        self.ADMIN_NAME = 'admin'
        self.PASSWORD_FOR_ADMIN = 'default'

    def setUp(self):
        self.db_fd, library.app.config['DATABASE'] = tempfile.mkstemp()
        library.app.config['TESTING'] = True
        self.app = library.app.test_client()
        library.init_db()

    def teardown(self):
        os.close(self.db_fd)
        os.unlink(library.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert rv.data != None

    def login(self, username, password):
        return self.app.post('/login',data = dict(
            username = username,
            password = password
            ), follow_redirects = True)

    def logout(self):
        return self.app.get('/logout', follow_redirects = True)

    def test_login_logout(self):
        """
        test if login or logout is OK
        """
        rv = self.login(self.ADMIN_NAME, self.PASSWORD_FOR_ADMIN)
        assert rv.data != None
        rv = self.logout()
        assert rv.data != None
        rv = self.login(self.ADMIN_NAME + 'a', self.PASSWORD_FOR_ADMIN)
        assert 'Invalid username' in rv.data
        rv = self.login(self.ADMIN_NAME, self.PASSWORD_FOR_ADMIN + 'a')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        """
        test if add new entry is OK
        """
        self.login(self.ADMIN_NAME, self.PASSWORD_FOR_ADMIN)
        rv = self.app.post('/add', data=dict(
            title = '<Hello>',
            text = '<strong>HTML</strong> allowed here'
            ), follow_redirects = True)
        assert rv.data != None
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__' :
    unittest.main()
