from flask import Flask, Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import datetime
from oauth import token_required
import jwt

user_bp = Blueprint('/', __name__, url_prefix='/')
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'teste'
app.config['DEBUG'] = True

# Criando novo user
@user_bp.route('/users', methods=['POST'])
def create_user():
  username = request.json['username']
  email = request.json['email']
  password = request.json['password']
  
  if username and email and password:
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': 'user created successfully', 'user': new_user.json()}), 201)
  else:
    return make_response(jsonify({'message': 'invalid data'}), 400)
  

# consultar todos dados
@user_bp.route('/users', methods=['GET'])
@token_required
def users():
  users = User.query.all()

  if users:
    return make_response(jsonify({'users': [user.json() for user in users]}), 200)
  else:
    return make_response(jsonify({'message': 'No users found'}), 404)

# consultar por id
@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
  user = User.query.filter_by(id = id).first()
  if user:
    return make_response(jsonify({'user': user.json()}), 200)
  return make_response(jsonify({'message': 'user not found'}), 404)

# editar usuario
@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
  data = request.get_json()
  username = data.get('username')
  email = data.get('email')
  password = data.get('password')
  user = User.query.get(id)
  if user:
    if username and email and password:
      hashed_password = generate_password_hash(password)
      user.username = username
      user.email = email
      user.password = hashed_password
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    else:
      return make_response(jsonify({'message': 'Missing fields'}), 400)
  else:
    return make_response(jsonify({'message': 'user not found'}), 404)

# excluir
@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.filter_by(id = id).first()
  if user:
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({'message': 'user deleted'}), 200)
  return make_response(jsonify({'message': 'user not found'}), 404)

############## auth test

@user_bp.route('/login', methods=['POST'])
def login():
  username = request.json['username']
  password = request.json['password']

  user = User.query.filter_by(username=username).first()

  if user and check_password_hash(user.password_hash, password):
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    jwt_token_encoded = jwt.encode({'id': user.id, 'exp': exp}, key=app.config['JWT_SECRET_KEY'], algorithm='HS256')

    response = jsonify(
      {'message': 'logged in succesfully', 
        'id': user.id, 
        'access_token': jwt_token_encoded, 
        'expiration_time': exp}
    )

    return response

  else:
    return make_response(jsonify({'message': 'Invalid username or password'}), 401)