from flask import jsonify, make_response
from werkzeug.security import generate_password_hash
from oauth import token_required
from models import User, login_model, user_model, user_input_model, register_model
from extensions import db, api
from flask_restx import Resource, Namespace

authorizations = {
  "jsonWebToken": {
      "type": "apiKey",
      "in": "header",
      "name": "Authorization"
  }
}

ns = Namespace("Users API", authorizations=authorizations)

@ns.route('/register')
class Register(Resource):
  @api.doc(description="Cria um novo usuário na API.")
  @api.expect(register_model)
  @api.response(201, "Usuário criado com sucesso.")
  @api.response(400, "Dados inválidos.")
  def post(self):
    username = api.payload['username']
    email = api.payload['email']
    password = api.payload['password']

    if username and email and password:
      hashed_password = generate_password_hash(password)
      new_user = User(username=username, email=email, password_hash=hashed_password)
      db.session.add(new_user)
      db.session.commit()
      return make_response(jsonify({'message': 'user created successfully', 'user': new_user.json()}), 201)
    else:
      return make_response(jsonify({'message': 'invalid data'}), 400)

@ns.route('/users')
class Users(Resource):
  method_decorators = [token_required]

  @api.expect(user_model)
  @api.doc(security="jsonWebToken", responses={200: 'OK', 404: 'Not Found'}, body=None)
  def get(self):
    users = User.query.all()
    if users:
      return make_response(jsonify({'users': [user.json() for user in users]}), 200)
    else:
      return make_response(jsonify({'message': 'No users found'}), 404)

@ns.route('/user/<int:id>')
@api.expect(user_model)
class UserById(Resource):
  # @api.marshal_with(user_model)
  def get(self, id):
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)

@ns.route('/update/<int:id>')
class UpdateUser(Resource):
  @api.expect(user_input_model)
  # @api.marshal_with(user_model)
  def put(self, id):
    data = api.payload
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user = User.query.get(id)
    if user:
      if username and email and password:
        hashed_password = generate_password_hash(password)
        user.username = username
        user.email = email
        user.password_hash = hashed_password
        db.session.commit()
        return make_response(jsonify({'message': 'user updated'}), 200)
      else:
        return make_response(jsonify({'message': 'Missing fields'}), 400)
    else:
      return make_response(jsonify({'message': 'user not found'}), 404)

@ns.route('/delete/<int:id>')
class DeleteUser(Resource):
  def delete(self, id):
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)

api.add_resource(Register, '/register')
api.add_resource(Users, '/users')
api.add_resource(UserById, '/user/<int:id>')
api.add_resource(UpdateUser, '/update/<int:id>')
api.add_resource(DeleteUser, '/delete/<int:id>')