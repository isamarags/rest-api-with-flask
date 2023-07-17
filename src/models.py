from extensions import db, api
from flask_restx import fields

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password_hash = db.Column(db.String(150), nullable=False)

  def __init__(self, username, email, password_hash):
    self.username = username
    self.email = email
    self.password_hash = password_hash

  def json(self):
    data = {
      'id': self.id,
      'username': self.username,
      'email': self.email
    }
    return data

login_model = api.model("LoginModel", {
    "username": fields.String,
    "password": fields.String
})

user_model = api.model("UserModel", {
    "id": fields.Integer(attribute='id'),  # Note the 'attribute' argument
    "username": fields.String(attribute='username'),  # Note the 'attribute' argument
    "email": fields.String(attribute='email')  # Note the 'attribute' argument
})


user_input_model = api.model("UserModel", {
    "username": fields.String(required=True),
    "email": fields.String(required=True)
})

register_model = api.model("RegisterModel", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
})