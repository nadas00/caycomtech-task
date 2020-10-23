from app import ma
from app.model import Customer
from marshmallow import fields, post_load

class CustomerSchema(ma.Schema):
    email = fields.Str(required=True, error_messages={"required": "Mail is required."})
    name = fields.Str(required=True, error_messages={"required": "Name is required."})
    surname = fields.Str(required=True, error_messages={"required": "Surname is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})
    identification_number = fields.Str(required=True, error_messages={"required": "Identification number is required."})
    phone_number = fields.Str(required=True, error_messages={"required": "Phone number is required."})

    class Meta:
        fields = ("id", "name", "surname", "email", "password", "identification_number", "phone_number")
    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
