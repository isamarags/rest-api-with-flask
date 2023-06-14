from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

user_bp = Blueprint('/', __name__, url_prefix='/')

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
# @jwt_required()
def users():
  users = User.query.all()
  return make_response(jsonify({'users': [user.json() for user in users]}), 200)

# consultar por id
@user_bp.route('/users/<int:id>', methods=['GET'])
# @jwt_required()
def get_user(id):
  user = User.query.filter_by(id = id).first()
  if user:
    return make_response(jsonify({'user': user.json()}), 200)
  return make_response(jsonify({'message': 'user not found'}), 404)

# editar usuario
@user_bp.route('/users/<int:id>', methods=['PUT'])
# @jwt_required()
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
@user_bp.route('/users/<int:id>', methods=['DELETE'])
# @jwt_required()
def delete_user(id):
  user = User.query.filter_by(id = id).first()
  if user:
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({'message': 'user deleted'}), 200)
  return make_response(jsonify({'message': 'user not found'}), 404)

############## auth test

@user_bp.route('/login', methods=['GET'])
def login():
  username = request.json['username']
  password = request.json['password']

  user = User.query.filter_by(username=username).first()

  if user and check_password_hash(user.password_hash, password):
    access_token = create_access_token(identity=user.id)

    user.access_token = access_token
    db.session.commit()

    return make_response(jsonify({'access_token': access_token}), 200)
  else:
    return make_response(jsonify({'message': 'Invalid username or password'}), 401)

# rota protegida que requer o token para acesso
@user_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
  current_user_id = get_jwt_identity()
  user = User.query.get(current_user_id)
  return make_response(jsonify({'user': user.json()}), 200)