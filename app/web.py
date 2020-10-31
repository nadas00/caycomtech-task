from flask import Flask, render_template, request, url_for, request, session
from app import app
from app import resource
import requests
import json


@app.route('/customers', methods = ["GET"])
def get_customers():
    url = 'http://127.0.0.1:8000/api/customers'
    headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDQxNTc0MTYsIm5iZiI6MTYwNDE1NzQxNiwianRpIjoiYWIyMmFiNzEtN2FkZS00MGViLWI0YzgtNDBkNDkyNmQ4ZTUxIiwiZXhwIjoxNjA0NzYyMjE2LCJpZGVudGl0eSI6IjIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.hH75HVFv41HoIHn7Feo6Xz8PC5efYyy4ispDRfLnywo'
    }
    print(session['token'])
    response = requests.request("GET", url, headers=headers).content
    json_response = json.loads(response)
    return render_template('customers.html', response = json_response)

@app.route('/customers/<string:id>', methods = ["GET"])
def get_customer(id):
    response = resource.CustomerResourceAPI.get(resource,id)
    return render_template('customers.html', response = response)

