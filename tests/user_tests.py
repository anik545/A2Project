import unittest
from flask_testing import TestCase
from app import app, db
from create_db import setup_database

from flask import url_for
from flask_login import current_user

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config')
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test_database.db'
        return app

    def setUp(self):
        setup_database()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class UserTest(BaseTestCase):

    def test_main_page(self):
        response = self.client.get(url_for('main'))
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        with self.client:

            response=self.client.post(url_for('user.login'),
                        data={'email':'hfreeman0@omniture.com', 'password':'Abc123'})

            self.assert_redirects(response, url_for('main'))
            self.client.get(url_for('user.logout'))
            self.assertTrue(current_user.is_anonymous)

    def test_fail_login(self):
        with self.client:
            response = self.client.post(url_for('user.login'),
                    data={'email':'hfreeman0@omniture.com', 'password':'abc123'})
            self.assertEqual(response.status_code, 200)

    def test_register(self):
        pass

    def test_fail_register_same_email(self):
        pass

    def test_fail_register_not_same_password(self):
        pass
