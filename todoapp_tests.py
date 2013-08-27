import unittest
from flask import json
import todoapp


class TodoAppTestCase(unittest.TestCase):

    def setUp(self):
        todoapp.app.config['TESTING'] = True
        self.app = todoapp.app.test_client()

    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', '111111')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data

    def add_memo(self, user_id, memo):
        return self.app.post('/memos/', data=dict(
            user_id=user_id,
            memo=memo
        ), follow_redirects=False)

    def get_memos(self, user_id):
        return self.app.get('/memos/' + str(user_id), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
