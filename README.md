# CaycomTech Application Task

##### Running directions:
* Open root folder
* Run "**python3 -m venv venv**"
* Run "**source venv/bin/activate**"
* Run "**pip install -r requirements.txt**"
* Run "**flask run**"

**If you facing anyproblem while running app you can contact me : se.hasanciftci@gmail.com**


All API points except register/login needs Bearer token.
> Sample user information for testing

```json
{
   "name":"caycom",
   "surname":"caycom",
   "email":"caycom",
   "password":"caycom",
   "phone_number":"caycom",
   "identification_number": "caycom"
}
```


## API Points

All api points are listed:
    
##### GET 
* **/customers** :
JWT Authorization needed route. List Customers.
* **/customers/<int:customer_id>** :
JWT Authorization needed route. Show customer by given id in route parameter.

##### POST 
* **/register** :
Register user.
* **/login** :
Login user. Returns a token.
> Sample request body for this route


```json
{
   "email":"caycom",
   "password":"caycom",
}
```

##### PATCH 
* **/customers/<int:customer_id>** :
JWT Authorization needed route. Patch user by given parameters.


##### DELETE 
* **/customers/<int:customer_id>** :
JWT Authorization needed route. Deletes user by id.

End of routes.
- INCLUDES UNIT TESTS:  /app/tests/test
    - SqlAlchemy Test Cases
    - Unauthorized Access Test Cases
    - Register Test Cases
    - Login Test Cases
    - Authorized Access Test Cases


> From root base terminal run **nose2** command to run tests.

- INCLUDES LOGGING:  /demo.log
#### Sample Token

```json
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDM1NDk3NTcsIm5iZiI6MTYwMzU0OTc1NywianRpIjoiZGQ3OTA3ZmUtOTcyZi00MDI0LWE2M2MtMGQwZDVmMjllYzhlIiwiZXhwIjoxNjA0MTU0NTU3LCJpZGVudGl0eSI6IjEiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.0tdDXse9cj7dAcS_L2OGdC3gMyNZ_Z6TaRixCKDTm5E
```
