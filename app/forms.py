from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    mail = StringField('Email', validators = [validators.DataRequired()])
    password = PasswordField('Password', validators = [validators.DataRequired()])