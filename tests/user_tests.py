import unittest
from flask import json
import todo
from todo.database import init_db, drop_all_table, create_all_table, db_session
from todo.routes import ResultType


class UsetTestCase(unittest.TestCase):
    def setUp(self):
        todo.app.config['TESTING'] = True
        self.app = todo.app.test_client()

    def tearDown(self):
        pass

    def setUpClass():
        # init_db('mysql+pymysql://root:123456@localhost/to_do2')
        create_all_table()
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

    def test_register_user_return_password_is_none_result(self):
        username = 'user_a'
        password = ''

        rv = self.register_user(username, password)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.PASSWORD_IS_NONE_ERRPR, result['result'])

    # test get user data
    def test_get_user_return_correct_result(self):
        username = 'user_for_get'
        password = '111111'

        self.register_user(username, password)

        rv = self.get_user(username)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.GET_USER_SECCESS, result['result'])

    def test_get_user_return_no_user_result(self):
        username = 'user_for_get_error'

        rv = self.get_user(username)
        result = json.loads(str(rv.data, 'utf-8'))
        self.assertEqual(ResultType.GET_USER_NO_DATA, result['result'])

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
