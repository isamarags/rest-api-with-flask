from flask import Flask, Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from oauth import token_required
from models import db, User

user_app_bp = Blueprint('/', __name__, url_prefix='/')

@user_app_bp.route('/users', methods=['POST'])
# class post(Resource):
  # @api.expect(model)
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

@user_app_bp.route('/users', methods=['GET'])
@token_required
def users(*args, **kwargs):
  users = User.query.all()

  if users:
    return make_response(jsonify({'users': [user.json() for user in users]}), 200)
  else:
    return make_response(jsonify({'message': 'No users found'}), 404)

@user_app_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
  user = User.query.filter_by(id = id).first()
  if user:
    return make_response(jsonify({'user': user.json()}), 200)
  return make_response(jsonify({'message': 'user not found'}), 404)

@user_app_bp.route('/user/<int:id>', methods=['PUT'])
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

@user_app_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.filter_by(id = id).first()
  if user:
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({'message': 'user deleted'}), 200)
  return make_response(jsonify({'message': 'user not found'}), 404)