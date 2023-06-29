from flask import Flask
from models import db
from Controller import userController, authController
from Controller.userController import user_app_bp as user_bp
from Controller.authController import auth_app_bp as auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/users'

with app.app_context():
  db.init_app(app)
  db.create_all()

app.register_blueprint(user_bp, name='user')
app.register_blueprint(auth_bp, name='auth')

if __name__ == "__main__":
  app.run(debug=True)