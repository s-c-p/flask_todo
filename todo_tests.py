import unittest
from flask import json
import todo
from todo.modules import db


class TodoTestCase(unittest.TestCase):

    def setUp(self):
        self.username = 'admin'
        self.password = '111111'
        self.new_memo = 'new_memo'
        todo.app.config['TESTING'] = True
        self.app = todo.app.test_client()

    def tearDown(self):
        pass

    def setUpClass():
        todo.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/to_do2'
        todo.init_db(todo.app)

    def tearDownClass():
        with todo.app.app_context():
            db.session.remove()
            db.drop_all()

    def register_user(self, username, password):
        return self.app.post('/users/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def get_user(self, username):
        return self.app.get('/users/' + username, follow_redirects=True)

    def delete_user(self, username):
        return self.app.delete('/users/' + username, follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.register_user(self.username, self.password)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(0, result['status'], 'register_user error')

        rv = self.login(self.username, self.password)
        self.assertIn(b'You were logged in', rv.data, 'logged in error')
        #rv = self.logout()
        #self.assertIn(b'You were logged out', rv.data, 'logged out error')

    def add_memo(self, user_id, memo):
        return self.app.post('/user/' + str(user_id) + '/memos/', data=dict(
            memo=memo
        ), follow_redirects=False)

    def get_memos(self, user_id):
        return self.app.get('/user/' + str(user_id) + '/memos/',
                            follow_redirects=True)

    def delete_memo(self, user_id, memo_id):
        return self.app.delete(
            '/user/' + str(user_id) + '/memos/' + str(memo_id),
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
        self.assertEqual(self.username, user['username'], 'get_user error')

        rv = self.add_memo(user['id'], 'test')
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertNotEqual(0, result['todo_memo_id'], 'add_memo error')

        rv = self.get_memos(user['id'])
        memos = json.loads(str(rv.data, 'utf-8'))
        self.assertLess(0, len(memos), 'get_memos erro')

        for memo in memos:
            rv = self.update_memo(memo['user_id'], memo['id'], self.new_memo)
            update_result = json.loads(str(rv.data, 'utf-8'))
            new_memo = json.loads(update_result['memo'])
            self.assertEqual(self.new_memo, new_memo['memo'], 'update_memo error')

        for memo in memos:
            rv = self.delete_memo(memo['user_id'], memo['id'])
            delete_result = json.loads(str(rv.data, 'utf-8'))
            self.assertEqual(0, delete_result['status'], 'delete_memo error')

        self.delete_user(self.username)

if __name__ == '__main__':
    unittest.main(verbosity=2)
