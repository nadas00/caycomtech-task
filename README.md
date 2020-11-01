# CaycomTech Application Task


##### Running directions:
* Open root folder
* Run "**python3 -m venv venv**"
* Run "**source venv/bin/activate**"
* Run "**pip install -r requirements.txt**"
* Run "**flask run**"

**If you facing anyproblem while running app you can contact me : se.hasanciftci@gmail.com**

# Web App
caycomtech-task Web App sends request to caycomtech-task API and renders responses.
### Routes:

###### Index (/) : 
redirects /login if no jwt. 
redirects /customer if jwt exists.

###### Logout (/logout) : 
kills session and jwt. 
redirects /login.

###### Register (/register) : 
registration page.
![](https://user-images.githubusercontent.com/46631211/97799701-af54ff80-1c40-11eb-9dbb-83cffc07e6b5.png)

###### Login (/login) : 
login page.
starts jwt session with successful login.
![](https://user-images.githubusercontent.com/46631211/97799734-d8759000-1c40-11eb-9620-31cfc9ae0ecc.png)

###### Customers (/customers) : 
show all customers in a table.
** jwt required route **
![](https://user-images.githubusercontent.com/46631211/97799762-fe9b3000-1c40-11eb-9ff4-b7cfaf66d07f.png)

###### Customers (/customers/< string:id >) : 
show a customer on a table row by id.
** jwt required route **
![](https://user-images.githubusercontent.com/46631211/97799790-1e325880-1c41-11eb-973d-8fec7d56468c.png)

###### Update (/update/< string:id >) : 
update a customer by id.
** jwt required route **
![](https://user-images.githubusercontent.com/46631211/97799830-4d48ca00-1c41-11eb-948b-4e0beca2960b.png)


###### Other errors (dynamic route):
returns error with message.
![](https://user-images.githubusercontent.com/46631211/97799816-3ace9080-1c41-11eb-83ba-251f2cedffef.png)

###### Delete (/delete/< string:id >) : 
delete a customer by id.
** jwt required route **


###### 404 (/404) : 
returns 404 with message.


# API

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
