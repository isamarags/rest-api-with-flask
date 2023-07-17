from flask import Flask
from extensions import db, api
from Controller.userController import ns as user_ns
from Controller.authController import ns as auth_ns

app = Flask(__name__)
api.init_app(app)

api.title = "Users API"
api.description = "API para gerenciamento de usuários"
api.version = "1.0"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/users'
with app.app_context():
  db.init_app(app)
  db.create_all()

api.add_namespace(user_ns)
api.add_namespace(auth_ns)

if __name__ == "__main__":
  app.run(debug=True)