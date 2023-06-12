from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/users'
db = SQLAlchemy(app)

class User(db.Model):

  id = db.Column(db.Integer, primary_key=True)

  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)

  def __init__(self, username, email, password_hash):
      self.username = username
      self.email = email
      self.password_hash = password_hash

  def json(self):
    return {'id': self.id, 'username': self.username, 'email': self.email}

with app.app_context():
  db.create_all()

# rota teste
@app.route('/teste', methods=['GET']) 
def test():
  return make_response(jsonify({'message': 'test route: funcionou'}), 200)  

# Criando novo user
@app.route('/users', methods=['POST'])
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
@app.route('/users', methods=['GET'])
def users():
  users = User.query.all()
  return make_response(jsonify({'users': [user.json() for user in users]}), 200)

# consultar por id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  user = User.query.filter_by(id = id).first()
  if user:
    return make_response(jsonify({'user': user.json()}), 200)
  return make_response(jsonify({'message': 'user not found'}), 404)

# editar usuario
@app.route('/users/<int:id>', methods=['PUT'])
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
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.filter_by(id = id).first()
  if user:
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({'message': 'user deleted'}), 200)
  return make_response(jsonify({'message': 'user not found'}), 404)

if __name__ == "__main__":
  app.run(debug=True)