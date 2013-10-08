import unittest
from flask import json
import todo
from todo.database import init_db, drop_all_table, db_session
from todo.routes import ResultType


class TodoTestCase(unittest.TestCase):

    def setUp(self):
        self.new_memo = 'new_memo'
        todo.app.config['TESTING'] = True
        self.app = todo.app.test_client()

    def tearDown(self):
        pass

    def setUpClass():
        # init_db('mysql+pymysql://root:123456@localhost/to_do2')
        pass

    def tearDownClass():

        if db_session:
            db_session.remove()

        drop_all_table()
        pass

    def register_user(self, username, password):
        return self.app.post('/todo/users/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def get_user(self, username):
        return self.app.get('/todo/users/' + username, follow_redirects=True)

    def delete_user(self, username):
        return self.app.delete('/todo/users/' + username, follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/todo/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/todo/logout', follow_redirects=True)

    def _test_login_logout(self):
        """
        test user action:
            1.register
            2.login
            3.logout
        """
        rv = self.register_user(self.username, self.password)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(0, result['status'], 'register_user error')

        rv = self.login(self.username, self.password)
        todo.app.logger.debug(json.loads(str(rv.data, 'utf-8')))
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(0, result['return_code'], 'logged error')

        rv = self.logout()
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(0, result['return_code'], 'logout error')

    def add_memo(self, user_id, memo):
        return self.app.post('/todo/user/' + str(user_id) + '/memos/', data=dict(
            memo=memo
        ), follow_redirects=False)

    def get_memos(self, user_id):
        return self.app.get('/todo/user/' + str(user_id) + '/memos/',
                            follow_redirects=True)

    def delete_memo(self, user_id, memo_id):
        return self.app.delete(
            '/todo/user/' + str(user_id) + '/memos/' + str(memo_id),
            follow_redirects=True)

    def update_memo(self, user_id, memo_id, memo, state='complete'):
        return self.app.put(
            '/todo/user/' + str(user_id) + '/memos/' + str(memo_id),
            data=dict(
            memo=memo,
            state=state
            ), follow_redirects=True)

    def _test_memo_operation(self):
        """
        test memo operation:
            1.add_memo
            2.get_memos
            3.update_memo
            4.delete_memo
        """
        rv = self.get_user(self.username)
        todo.app.logger.debug(json.loads(str(rv.data, 'utf-8')))
        result = json.loads(str(rv.data, 'utf-8'))
        user = json.loads(result['user'])
        self.assertEqual(self.username, user['username'], 'get_user error')

        rv = self.add_memo(user['id'], 'test')
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertNotEqual(0, result['todo_memo_id'], 'add_memo error')

        rv = self.get_memos(user['id'])
        result = json.loads(str(rv.data, 'utf-8'))
        memos = result['memos']
        todo.app.logger.debug('memos :{0}'.format(memos))
        self.assertLess(0, len(memos), 'get_memos erro')

        for memo in memos:
            rv = self.update_memo(memo['user_id'], memo['id'], self.new_memo)
            todo.app.logger.debug(json.loads(str(rv.data, 'utf-8')))
            update_result = json.loads(str(rv.data, 'utf-8'))
            new_memo = json.loads(update_result['memo'])
            self.assertEqual(
                self.new_memo, new_memo['memo'], 'update_memo error')

        for memo in memos:
            rv = self.delete_memo(memo['user_id'], memo['id'])
            delete_result = json.loads(str(rv.data, 'utf-8'))
            self.assertEqual(0, delete_result['status'], 'delete_memo error')

        self.delete_user(self.username)

    # test register
    def test_register_user_return_correct_result(self):
        username = 'user_a'
        password = '111111'

        rv = self.register_user(username, password)
        result = json.loads(str(rv.data, 'utf-8'))
        # todo.app.logger.debug('result : {0}'.format(result))
        self.assertEqual(ResultType.REGISTER_SECCESS, result['result'])

    def test_register_user_return_username_is_exist_result(self):
        username = 'user_b'
        password = '111111'

        rv = self.register_user(username, password)
        rv = self.register_user(username, password)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.USER_EXIST_ERROR, result['result'])

    def test_register_user_return_username_is_none_result(self):
        username = ''
        password = '111111'

        rv = self.register_user(username, password)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.USERNAME_IS_NONE_ERROR, result['result'])

    def test_register_uset_return_password_is_none_result(self):
        username = 'user_a'
        password = ''

        rv = self.register_user(username, password)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.PASSWORD_IS_NONE_ERRPR, result['result'])

    # test login
    def test_login_return_correct_result(self):
        username = 'user_c'
        password = '111111'

        # register user
        self.register_user(username, password)

        # login user
        rv = self.login(username, password)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.LOGIN_SECCESS, result['result'])

    def test_login_return_no_user_result(self):
        username = 'user_none'
        password = '111111'
        rv = self.login(username, password)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.LOGIN_NO_USER_DATA, result['result'])

    def test_login_return_password_error_result(self):
        username = 'user_d'
        password = '111111'

        # register user
        self.register_user(username, password)
        # login user
        password_error = '222222'
        rv = self.login(username, password_error)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.LOGIN_PASSWORD_ERROR, result['result'])


    def _test_add_memo_return_correct_result(self):
        pass

    def _test_add_memo_return_no_user_error_result(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
