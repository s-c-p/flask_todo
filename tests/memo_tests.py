import unittest
from flask import json
import todo
from todo.database import init_db, drop_all_table, create_all_table, db_session
from todo.routes import ResultType


class MemoTestCase(unittest.TestCase):

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

    # test add memo
    def test_add_memo_return_correct_result(self):
        username = 'user_e'
        password = '111111'

        # register user
        self.register_user(username, password)
        get_user_rv = self.get_user(username)
        get_user_result = json.loads(str(get_user_rv.data, 'utf-8'))
        user = get_user_result['user']

        # add memo
        add_memo_rv = self.add_memo(user['id'], 'test')
        add_memo_result = json.loads(str(add_memo_rv.data, 'utf-8'))
        self.assertEqual(
            ResultType.ADD_MEMO_SECCESS, add_memo_result['result'])

    def test_add_memo_return_no_user_error_result(self):
        add_memo_rv = self.add_memo(9999999, 'test')
        add_memo_result = json.loads(str(add_memo_rv.data, 'utf-8'))
        self.assertEqual(
            ResultType.ADD_MEMO_NO_USER_DATA, add_memo_result['result'])

    # test get memos
    def test_get_memos_return_correct_result(self):
        username = 'user_for_get_memos'
        password = '111111'

        # register user
        self.register_user(username, password)
        get_user_rv = self.get_user(username)
        get_user_result = json.loads(str(get_user_rv.data, 'utf-8'))
        user = get_user_result['user']

        # add memo
        self.add_memo(user['id'], 'test')

        # get memos
        get_memos_rv = self.get_memos(user['id'])
        get_memos_result = json.loads(str(get_memos_rv.data, 'utf-8'))
        self.assertEqual(
            ResultType.GET_MEMOS_SECCESS, get_memos_result['result'])

    def test_get_memos_return_no_user_error_result(self):
        # get memos
        get_memos_rv = self.get_memos(0)
        get_memos_result = json.loads(str(get_memos_rv.data, 'utf-8'))
        self.assertEqual(
            ResultType.GET_MEMOS_NO_USER_DATA, get_memos_result['result'])

    # test_update_memo
    def test_update_memo_return_correct_result(self):
        username = 'user_for_update_memo'
        password = '111111'

        # register user
        self.register_user(username, password)
        get_user_rv = self.get_user(username)
        get_user_result = json.loads(str(get_user_rv.data, 'utf-8'))
        user = get_user_result['user']

        # add memo
        self.add_memo(user['id'], 'test')

        # get memos
        get_memos_rv = self.get_memos(user['id'])
        get_memos_result = json.loads(str(get_memos_rv.data, 'utf-8'))
        memos = get_memos_result['memos']
        for memo in memos:
            update_memo_rv = self.update_memo(memo['user_id'], memo['id'],
                                              'new_memo')
            update_result = json.loads(str(update_memo_rv.data, 'utf-8'))
            self.assertEqual(
                ResultType.UPDATE_MEMO_SECCESS, update_result['result'])

    def test_update_memo_return_no_user_error_result(self):
        update_memo_rv = self.update_memo(0, 0, 'new_memo')
        update_result = json.loads(str(update_memo_rv.data, 'utf-8'))
        self.assertEqual(
            ResultType.UPDATE_MEMO_NO_USER_DATA, update_result['result'])

    def test_update_memo_return_no_memo_data_result(self):
        username = 'user_for_update_memo_a'
        password = '111111'

        # register user
        self.register_user(username, password)
        get_user_rv = self.get_user(username)
        get_user_result = json.loads(str(get_user_rv.data, 'utf-8'))
        user = get_user_result['user']

        update_memo_rv = self.update_memo(user['id'], 0, 'new_memo')
        update_result = json.loads(str(update_memo_rv.data, 'utf-8'))
        self.assertEqual(
            ResultType.UPDATE_MEMO_NO_MEMO_DATA, update_result['result'])

    def test_delete_memo_return_correct_result(self):
        username = 'user_for_delete_memo'
        password = '111111'

        # register user
        self.register_user(username, password)
        get_user_rv = self.get_user(username)
        get_user_result = json.loads(str(get_user_rv.data, 'utf-8'))
        user = get_user_result['user']

        # add memo
        self.add_memo(user['id'], 'test')

        # get memos
        get_memos_rv = self.get_memos(user['id'])
        get_memos_result = json.loads(str(get_memos_rv.data, 'utf-8'))
        memos = get_memos_result['memos']

        for memo in memos:
            delete_memo_rv = self.delete_memo(memo['user_id'], memo['id'])
            delete_result = json.loads(str(delete_memo_rv.data, 'utf-8'))
            self.assertEqual(
                ResultType.DELETE_MEMO_SECCESS, delete_result['result'])

    def test_delete_memo_return_no_user_error_result(self):
        delete_memo_rv = self.delete_memo(0, 0)
        delete_result = json.loads(str(delete_memo_rv.data, 'utf-8'))
        self.assertEqual(
            ResultType.DELETE_MEMO_NO_USER_DATA, delete_result['result'])

    def test_delete_memo_return_no_memo_data_result(self):
        username = 'user_for_delete_memo_A'
        password = '111111'

        # register user
        self.register_user(username, password)
        get_user_rv = self.get_user(username)
        get_user_result = json.loads(str(get_user_rv.data, 'utf-8'))
        user = get_user_result['user']

        delete_memo_rv = self.delete_memo(user['id'], 0, )
        delete_result = json.loads(str(delete_memo_rv.data, 'utf-8'))
        self.assertEqual(
            ResultType.DELETE_MEMO_NO_MEMO_DATA, delete_result['result'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
