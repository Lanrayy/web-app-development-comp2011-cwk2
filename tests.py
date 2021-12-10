import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        # client.post('/login', data={'username':'bob', 'password':'b'})
        pass


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ##### HELPER ######
    def register(self, name, username, password, password2):
        return self.app.post('/register',data=dict(name=name, username=username,
        password1=password,
        password2=password2),
        follow_redirects=True
        )

    def login(self, username, password):
        return self.app.post('/login',data=dict(email=email, password=password),
        follow_redirects=True)

    def logout(self):return self.app.get('/logout',follow_redirects=True)

    ##########

    def test_valid_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', content_type='html/text', data=dict(username="bob", password="test",
        follow_redirects=True))

        self.assertIn(b'Dashboard' in response.data)
    #test webpage redirects to login page
    def test_loginroute(self):
        response = self.app.get('/login',follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Login' in response.data)

    def test_loginroute(self, ):
        response = self.app.get('/login',follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_indexroute(self):
        response = self.app.get('/',follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logoutroute(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signuproute(self):
        response = self.app.get('/signup',follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_dashboardroute(self):
    #     response = self.app.get('/dashboard',follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)





if __name__ == '__main__':
    unittest.main()
