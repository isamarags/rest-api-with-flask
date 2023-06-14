from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from models import db
from Controller import userController
from Controller.userController import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/users'
app.config['JWT_SECRET_KEY'] = 'teste'  # Chave secreta para assinatura do token JWT

db.init_app(app)
# oauth = OAuth2Provider(app)
jwt = JWTManager(app)

with app.app_context():
  db.create_all()

app.register_blueprint(user_bp)

if __name__ == "__main__":
  app.run(debug=True)