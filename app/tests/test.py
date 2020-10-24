import unittest
import json
import sys

from app import db, app
from app.model import Customer
from sqlalchemy.exc import IntegrityError

class SqlAlchemyTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_customer_model(self):
        c = Customer(name="aaa", surname="bbb", email="ccc", password="ddd", phone_number="eee", identification_number="fff")
        self.assertEqual(c.name, 'aaa')
        self.assertEqual(c.surname, 'bbb')
        self.assertEqual(c.email, 'ccc')
        self.assertEqual(c.password, 'ddd')
        self.assertEqual(c.phone_number, 'eee')
        self.assertEqual(c.identification_number, 'fff')
     

    def test_customer_model_password_encrypt_and_verify(self):
        c = Customer(name="aaa", surname="bbb", email="ccc", phone_number="eee", identification_number="fff")
        c.create_password('ddd')
        passwords_matched  = c.check_password('ddd')

        self.assertEqual(passwords_matched, True)

    def test_deny_duplicated_email(self):
        c = Customer(name="aaa", surname="aaa", email="samemail", password="aaa", phone_number="aaa", identification_number="aaa")
        email = c.email
        db.session.add(c)
        c = Customer(email="samemail", name="aaa", surname="aaa", password="aaa", phone_number="aaa", identification_number="aaa")
        db.session.add(c)
        
        self.assertRaises(IntegrityError, db.session.commit)
            
    def test_customer_model_with_missing_data(self):
        c = Customer(name="aaa")
        db.session.add(c)
        self.assertRaises(IntegrityError, db.session.commit)

class UnauthorizedAccessTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unauthorized_access_to_customers(self):
        response = self.app.get('/customers')
        self.assertEqual(response.status_code,401)
        
    def test_unauthorized_access_to_single_customer(self):
        response = self.app.get('/customers/1')
        self.assertEqual(response.status_code,401)

    def test_unauthorized_access_to_delete_single_customer(self):
        response = self.app.delete('/customers/1')
        self.assertEqual(response.status_code,401)

    def test_unauthorized_access_to_patch_single_customer(self):
        response = self.app.patch('/customers/1')
        self.assertEqual(response.status_code,401)

class RegisterTestsCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        response = self.app.post('/register', json={"name":"aaa","surname":"aaa","email":"aaa","password":"aaa","phone_number":"aaa","identification_number": "aaa"})
        self.assertEqual(response.status_code, 200)

    def test_register_with_missing_data(self):
            response = self.app.post('/register', json={'email': 'aaa', 'password': 'aaa'})
            self.assertEqual(response.status_code, 400)
    
    def test_register_with_already_registered_mail(self):
        c = Customer(name="aaa", surname="aaa", email="samemail", password="aaa", phone_number="aaa", identification_number="aaa")
        db.session.add(c)
        db.session.commit()
        response = self.app.post('/register', json={"name":"aaa","surname":"aaa","email":"samemail","password":"aaa","phone_number":"aaa","identification_number": "aaa"})
        self.assertEqual(response.status_code, 409)
            
class LoginTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

        #Sample User1
        c = Customer(name="aaa", surname="bbb", email="ccc", phone_number="eee", identification_number="fff")
        c.create_password('rightpassword')
        db.session.add(c)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        #test with Sample User1
        response = self.app.post('/login', json={"email": "ccc", "password":"rightpassword"})
        self.assertEqual(response.status_code, 200)
    
    def test_login_with_wrong_password(self):
        #test with Sample User1
        response = self.app.post('/login', json={"email": "ccc", "password":"wrongpassword"})
        self.assertEqual(response.status_code, 401)

    def test_login_with_missing_data(self):
        response = self.app.post('/login', json={'email': 'aaa'})
        self.assertEqual(response.status_code, 400)

class AuthorizedAccessTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

        #Sample User2
        c = Customer(name="aaa", surname="bbb", email="ccc", phone_number="eee", identification_number="fff")
        c.create_password('rightpassword')
        db.session.add(c)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all() 

    def test_auth(self):
        #get token with Sample User2
        global token 
        response = self.app.post('/login', json={"email": "ccc", "password":"rightpassword"})
        token = json.loads(response.get_data().decode(sys.getdefaultencoding()))['token']
        assert token != None

    def test_authorized_access_to_customers(self):
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.app.get('/customers',headers=headers)

        self.assertEqual(response.status_code,200)
        
    def test_authorized_access_to_single_customer(self):
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.app.get('/customers/1',headers=headers)

        self.assertEqual(response.status_code,200)

    def test_authorized_access_to_delete_single_customer(self):
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.app.delete('/customers/1',headers=headers)

        self.assertEqual(response.status_code,204)

    def test_authorized_access_to_patch_single_customer(self):
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.app.patch('/customers/1', json={"email": "bbb", "password":"rightpassword"},headers=headers)
        
        self.assertEqual(response.status_code,200)
  
if __name__ == '__main__':
    unittest.main()