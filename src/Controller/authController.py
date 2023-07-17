from flask import jsonify, request, make_response, Flask
import jwt
import datetime
from models import User, login_model
from extensions import api
from werkzeug.security import check_password_hash
from flask_restx import Resource, fields, Namespace

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'teste'
app.config['DEBUG'] = True

authorizations = {
  "jsonWebToken": {
    "type": "apiKey",
    "in": "header",
    "name": "Authorization"
    }
}

ns = Namespace("Auth API", authorizations=authorizations)

@ns.route('/login')
class Login(Resource):
  @api.expect(login_model)
  def post(self):
    username = api.payload['username']
    password = api.payload['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
      exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
      jwt_token_encoded = jwt.encode({'id': user.id, 'exp': exp}, key=app.config['JWT_SECRET_KEY'], algorithm='HS256')

      response_data = {
        'message': 'logged in successfully',
        'id': user.id,
        'access_token': jwt_token_encoded,
        'expiration_time': exp.isoformat(),
      }

      return response_data

    else:
      return make_response(jsonify({'message': 'Invalid username or password'}), 401)

api.add_resource(Login, '/login')