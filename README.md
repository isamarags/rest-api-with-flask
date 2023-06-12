<h1>Login Rest API</h1>
RESTful API using Python Flask that allows users to login in a platform.
<br> <br>

### Requirements
```bash
pip install -r requirements.txt
```

### Usage

Start the server:

`python app.py` (Starts the server on 127.0.0.1:5000)

To test the API using Postman, install postman agent in your OS and call the API using Postman.

### Endpoints

#### Fetch products using name, category, subcategory
- [GET] `/teste` - Get test: `test`
<br></br>
- [GET] `/users` - Get all users
<br></br>
- [GET] `/users/<id: int>` - Get user with id: `id`
<br></br>

- [PUT] `/users/(int: id)` - Update user with id
```
{
  "username": "username",
  "email": "email",
  "password": "password"
}
```

- [POST] `/users` - Create a new user
```
{
  "username": "username",
  "email": "email",
  "password": "password" // hashed
}
```

- [DELETE] `/users/(int: id)` - Delete user with id