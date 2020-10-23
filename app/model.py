from app import db
from passlib.handlers.sha2_crypt import sha256_crypt

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    identification_number = db.Column(db.String(11))
    phone_number = db.Column(db.String(10))

    def create_password(self,password):
        self.password = sha256_crypt.encrypt(password)
    def check_password(self,password):
        return sha256_crypt.verify(password,self.password)
    def __repr__(self):
        return '<Customer %s>' % self.email