from app import app
import unittest


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        tester = app.test_client(self)
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_user_api(self):
        tester = app.test_client(self)
        response = tester.get('/user/<username>', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        tester = app.test_client(self)
        response = tester.get('/edit_profile', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_explore(self):
        tester = app.test_client(self)
        response = tester.get('/explore', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
  unittest.main()
