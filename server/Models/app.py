from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .routes import api

db=SQLAlchemy()
bcrypt =  Bcrypt()
jwt = JWTManager()
migrate = Migrate()
cors= CORS()

def create_app():
  app = Flask(__name__)

  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ajali_user:aJali!@localhost/ajali_db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = 'your-secret-key'
  
  bcrypt.init_app(app)
  db.init_app(app)
  jwt.init_app(app)
  migrate.init_app(app,db)
  cors.init_app(app)

  # from routes import api as api_bp
  # app.register_blueprint(api_bp, url_prefix='/api')
  from .routes import api
  app.register_blueprint(api)
  
  return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)