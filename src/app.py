from flask import Flask
from models import db
from Controller import userController
from Controller.userController import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/users'

db.init_app(app)

with app.app_context():
  db.create_all()

app.register_blueprint(user_bp)

if __name__ == "__main__":
  app.run(debug=True)