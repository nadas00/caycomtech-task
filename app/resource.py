from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from app import api, db
from app.model import Customer
from app.schema import customers_schema, customer_schema, CustomerSchema
from marshmallow import ValidationError
from flask import request
import datetime
import logging

class CustomerListResource(Resource):
    @jwt_required
    def get(self):
        logging.info(msg="Show all customers API point")
        customers = Customer.query.all()
        logging.info(msg="Customers listed")
        return customers_schema.dump(customers)


class CustomerResource(Resource):
    @jwt_required
    def get(self, customer_id):
        logging.info(msg="Show customer by id API point")
        customer = Customer.query.get_or_404(customer_id)
        return customer_schema.dump(customer)

    @jwt_required
    def patch(self, customer_id):
        logging.info(msg="Patch customer by id API point")
        customer = Customer.query.get_or_404(customer_id)
        if 'name' in request.json:
            customer.name = request.json['name']
        if 'surname' in request.json:
            customer.surname = request.json['surname']
        if 'identification_number' in request.json:
            customer.identification_number = request.json['identification_number']
        if 'phone_number' in request.json:
            customer.phone_number = request.json['phone_number']
        if 'email' in request.json:
            if customer.email != request.json['email']:
                if customer_exists(request.json['email']):
                    logging.error(msg="Email already exists")
                    return {'Error': 'Customer with this email already exists'}, 409
                customer.email = request.json['email']
        if 'password' in request.json:
            customer.create_password(request.json['password'])
        logging.info(msg="Customer patch operation success")
        db.session.commit()
        return customer_schema.dump(customer)

    @jwt_required
    def delete(self, customer_id):
        logging.info(msg="Delete single customer by id API piont")
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        logging.info(msg="Customer delete operation success")
        return '', 204


class RegisterApiResource(Resource):
    def post(self):
        try:
            result = CustomerSchema().load(request.json)
        except ValidationError as err:
            logging.error(msg="Error occured while registering proccess")
            return {"error": err.messages}, 400

        new_customer = Customer(
            name=request.json['name'],
            surname=request.json['surname'],
            email=request.json['email'],
            phone_number=request.json['phone_number'],
            identification_number=request.json['identification_number']
        )
        new_customer.create_password(request.json['password'])

        if customer_exists(new_customer.email):
            logging.error(msg="Customer with this email already exists")
            return {'Error': 'Customer with this email already exists'}, 409
        db.session.add(new_customer)
        db.session.commit()
        logging.info(msg="New customer registered")
        return customer_schema.dump(new_customer)


class LoginApiResource(Resource):
    def post(self):
        if "email" in request.json and "password" in request.json:
            customer = Customer.query.filter_by(email = request.json["email"]).first()
            if customer is None:
                logging.error(msg="Login process user not found")
                return {"Error":"User not found!"}
            authorized = customer.check_password(request.json["password"])
            if not authorized:
                logging.error(msg="Login process password is wrong")
                return {'error': 'Email or password invalid'}, 401
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(customer.id), expires_delta=expires)
            logging.info(msg="Login process success token created.")
            return {'token': access_token}, 200
        return {'Error': 'email and password fields needed'}, 400

api.add_resource(CustomerListResource, '/customers')
api.add_resource(CustomerResource, '/customers/<int:customer_id>')
api.add_resource(RegisterApiResource, '/register')
api.add_resource(LoginApiResource, '/login')


def customer_exists(email):
    return Customer.query.filter(Customer.email == email).first() is not None
