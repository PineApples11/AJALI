from flask import Flask
from Models.extensions import db, bcrypt, jwt, migrate, cors
from Models.routes import api
import os

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ajali_user:aJali!@localhost/ajali_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret')

    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    app.register_blueprint(api)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)