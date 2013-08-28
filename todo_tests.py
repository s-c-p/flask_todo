import unittest
from flask import json
import todo


class TodoTestCase(unittest.TestCase):

    def setUp(self):
        todo.app.config['TESTING'] = True
        self.app = todo.app.test_client()

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

    def test_memo_opration(self):
        rv = self.add_memo(1, 'test')
        result = json.loads(str(rv.data, 'utf-8'))
        assert 0 == result['status']

        rv = self.get_memos(1)
        result = json.loads(str(rv.data, 'utf-8'))

        memos = [json.loads(memo) for memo in json.loads(result.get('memos'))]

        for memo in memos:
            assert 1 == memo['user_id']
            assert 'test' == memo['memo']

if __name__ == '__main__':
    unittest.main(verbosity=2)
