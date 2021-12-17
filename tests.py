import os
import unittest
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
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

    #get signup test
    data={'name': 'Mike', 'username':'mike', 'password': 'test', 'password2':'test' }
    #get login test
    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        print('Login route test completed')
        pass
    
    #get signup test
    def test_signup_route(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        print('Signup route test completed')
        pass

    # get account test
    def test_account_get_route(self):
        response = self.app.get('/account')
        self.assertEqual(response.status_code, 200)
        print('Account get route test completed')
        pass

    
    # get add module test
    def test_add_module_get_route(self):
        response = self.app.get('/add_module')
        self.assertEqual(response.status_code, 200)
        print('Add module get route test completed')
        
    # get edit password test
    def test_edit_password_get_route(self):
        response = self.app.get('/edit_password')
        self.assertEqual(response.status_code, 200)
        print('Edit password get route test completed')
        pass

    # get index test
    def test_index_get_route(self):
        response = self.app.get('/index')
        self.assertEqual(response.status_code, 200)
        print('Index get route test completed')
        pass
    

    








if __name__ == '__main__':
    unittest.main()
