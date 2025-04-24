from flask_bcrypt import Bcrypt
bcrypt =  Bcrypt()

def create_app():
  app = Flask(__name__)
  bcrypt.init_app(app)
  return app