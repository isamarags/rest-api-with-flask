# Login Rest API
This is a RESTful API using Python Flask that allows users to login to a platform.
<br>

### Requirements
- Python 3
  
- PostgreSQL

## Installation
<br>
1. Install pipenv package manager:
` $ python -m venv .venv `
<br>

#### Install libraries and binaries:
`$.venv\Scripts\activate` (for Windows)
or
`$ source .venv/bin/activate` (for Linux/Mac)

<br>

Install required libraries and dependencies:
```
pip install -r requirements.txt
```

### Usage

Start the server:

`python app.py` 
This will start the server on `http://127.0.0.1:5000`.

To test the API, you can use tools like Postman to make API calls.
<br>

### API Documentation

The API is documented using Swagger. To access the documentation, go to  `http://127.0.0.1:5000` in your web browser. 
This will open the Swagger UI, where you can explore all the available endpoints, see their parameters, and make test requests.
<br>

### Endpoints

#### Fetch users

- Create a new user - [POST] `/register` 
```
{
  "username": "username",
  "email": "email",
  "password": "password" // hashed
}
```
<br>

- Login a new user - [POST] `/login`
```
{
  "username": "username",
  "password": "password"
}
```
<br>

- Get all users - [GET] `/users`
Returns a list of all registered users.

<br>

- Get user by id - [GET] `/users/<id: int>`
Returns the user with the specified ID.
<br>

- Update user - [PUT] `/update/(int: id)` - 
```
{
  "username": "username",
  "email": "email",
  "password": "password"
}
```
Updates the user with the specified ID.
<br>

- Delete user - [DELETE] `/delete/(int: id)` 
Deletes the user with the specified ID.

<br>

### Explanation
This API has several features and is organized into different files:

- app.py: The entry point of the Flask application, where the API is initialized and routes are defined.
- models.py: Contains the definition of the User class that represents a user model, mapped to the database using SQLAlchemy.
- extensions.py: Initializes the Flask extensions such as SQLAlchemy and Flask-RESTx (for creating the API).
- oauth.py: Implements token-based authentication with JWT, ensuring that certain routes are accessible only to authenticated users.
#### Controllers:
- userController.py: Defines the API controllers related to user operations, such as registration, retrieval, update, and deletion.
- authController.py: Defines the authentication controller, allowing users to log in and receive a valid JWT token.
  <br>
The API uses a PostgreSQL database, and SQLAlchemy handles database access. The endpoints for creating, updating, and deleting users are protected and require a valid JWT token to access.
