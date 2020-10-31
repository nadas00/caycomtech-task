from flask import Flask, render_template, request, url_for, request, session, redirect
from app import app
from app import resource
import requests
import json
from app.forms import LoginForm, RegisterForm, UpdateForm


@app.route('/customers', methods = ["GET"])
def get_customers():
    url = 'http://127.0.0.1:8000/api/customers'
    response = requests.request("GET", url, headers=set_headers())
    json_response = json.loads(response.content)
    if response.status_code == 200:
        return render_template('customers.html', response = json_response)
    return render_template('customers.html', response = json_response, error = 'Error')

@app.route('/customers/<string:id>', methods = ["GET"])
def get_customer(id):
    url = 'http://127.0.0.1:8000/api/customers/'+id
    response = requests.request("GET", url, headers=set_headers())
    json_response = [json.loads(response.content)]
    if response.status_code == 200:
        return render_template('customers.html', response = json_response)
    return render_template('customers.html', response = json_response, error = 'Error')


@app.route('/login', methods = ["GET","POST"])
def login():

    if "logged_in" in session:
        return redirect(url_for('get_customers'))

    url = 'http://127.0.0.1:8000/api/login'
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        entered_email = form.mail.data
        entered_password = form.password.data
        response = requests.request("POST", url, json={"email":entered_email, "password":entered_password})
        json_response = json.loads(response.content)
    
        if response.status_code == 200:
            session['token'] = json_response['token']
            session['logged_in'] = True
            return redirect(url_for('index'))

        return render_template('404.html', response = json_response, status=response.status_code)
    return render_template('login.html',form = form)

@app.route('/register', methods = ["GET","POST"])
def register():
    url = 'http://127.0.0.1:8000/api/register'
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        entered_email = form.mail.data
        entered_password = form.password.data
        entered_name = form.name.data
        entered_surname = form.surname.data
        entered_phone_no = form.phone_no.data
        entered_id_no = form.id_no.data
        response = requests.request("POST", url, json={"email":entered_email, "password":entered_password, "name":entered_name, "surname":entered_surname, "identification_number":entered_id_no, "phone_number":entered_phone_no})
        json_response = json.loads(response.content)

        if response.status_code == 201:
            return redirect(url_for('index'))

        return render_template('404.html', response = json_response, status=response.status_code)
    return render_template('register.html',form=form)

@app.route('/delete/<string:id>')
def delete(id):
    url = 'http://127.0.0.1:8000/api/customers/'+id
    response = requests.request("DELETE", url, headers=set_headers())
    return redirect(url_for('index'))

@app.route('/update/<string:id>', methods = ["GET","POST"])
def update(id):
    form = UpdateForm(request.form)
    if request.method == "POST" and form.validate():
        url = 'http://127.0.0.1:8000/api/customers/'+id
        entered_email = form.mail.data
        entered_name = form.name.data
        entered_surname = form.surname.data
        entered_phone_no = form.phone_no.data
        entered_id_no = form.id_no.data
        response = requests.request("PATCH", url, headers=set_headers(), json={"email":entered_email, "name":entered_name, "surname":entered_surname, "identification_number":entered_id_no, "phone_number":entered_phone_no})
        json_response = json.loads(response.content)
        if response.status_code == 200:
            return redirect(url_for('index'))
        return render_template('404.html', response = json_response, status=response.status_code)
    return render_template('update.html', form = form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    if "logged_in" in session:
        return redirect(url_for('get_customers'))
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
   

def set_headers():
    headers = {}
    if 'token' in session:
        headers = {'Authorization': 'Bearer {}'.format(session['token'])}
    return headers