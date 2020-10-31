from flask import Flask, render_template, request, url_for, request, session
from app import app
from app import resource
import requests
import json
from app.forms import LoginForm


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
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        pass
    return render_template('login.html',form = form)
   

def set_headers():
    headers = {}
    if 'token' in session:
        headers = {'Authorization': 'Bearer {}'.format(session['token'])}
    return headers