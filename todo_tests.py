import unittest
from flask import json
import todo
from todo.modules import User


class TodoTestCase(unittest.TestCase):

    def setUp(self):
        self.username = 'admin'
        self.password = '111111'
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
        rv = self.login(self.username, self.password)
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data

    def get_user(self, username):
        return self.app.get('/users/' + username, follow_redirects=True)

    def add_memo(self, user_id, memo):
        return self.app.post('/user/' + str(user_id) + '/memos/', data=dict(
            memo=memo
        ), follow_redirects=False)

    def get_memos(self, user_id):
        return self.app.get('/user/' + str(user_id) + '/memos/',
                            follow_redirects=True)

    def delete_memo(self, user_id, memo_id):
        return self.app.delete('/user/' + str(user_id) + '/memos/' + str(memo_id),
            follow_redirects=True)

    def update_memo(self, user_id, memo_id, memo):
        return self.app.put('/user/' + str(user_id) + '/memos/' + str(memo_id),
        data=dict(
            memo=memo
        ), follow_redirects=True)

    def test_memo_operation(self):
        rv = self.get_user(self.username)
        result = json.loads(str(rv.data, 'utf-8'))
        user = json.loads(result['user'])
        assert self.username == user['username']

        rv = self.add_memo(user['id'], 'test')
        result = json.loads(str(rv.data, 'utf-8'))
        assert 0 == result['status']

        rv = self.get_memos(user['id'])
        result = json.loads(str(rv.data, 'utf-8'))

        memos = [json.loads(memo) for memo in json.loads(result.get('memos'))]

        assert 0 < len(memos)

        for memo in memos:
            rv = self.update_memo(memo['user_id'], memo['id'], 'new_memo')
            update_result = json.loads(str(rv.data, 'utf-8'))
            new_memo = json.loads(update_result['memo'])
            assert 'new_memo' == new_memo['memo']

        for memo in memos:
            rv = self.delete_memo(memo['user_id'], memo['id'])
            delete_result = json.loads(str(rv.data, 'utf-8'))
            assert 0 == delete_result['status']

if __name__ == '__main__':
    unittest.main(verbosity=2)
