from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    mail = StringField('Email', validators = [validators.DataRequired()])
    password = PasswordField('Password', validators = [validators.DataRequired()])


class RegisterForm(Form):
    mail = StringField('Email', validators = [validators.DataRequired()])
    password = PasswordField('Password', validators = [validators.DataRequired()])
    name = StringField('Name', validators = [validators.DataRequired()])
    surname = StringField('Surname', validators = [validators.DataRequired()])
    id_no = StringField('TC No', validators = [validators.DataRequired()])
    phone_no = StringField('Phone No', validators = [validators.DataRequired()])
    
    