from flask import Flask, jsonify, request, make_response, Blueprint
import jwt
import datetime
from models import User
from werkzeug.security import check_password_hash

auth_app_bp = Blueprint('/', __name__, url_prefix='/')
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'teste'
app.config['DEBUG'] = True

@auth_app_bp.route('/login', methods=['POST'])
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
