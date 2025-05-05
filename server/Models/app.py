from flask import Flask
from Models.extensions import db, bcrypt, jwt, migrate, cors
from Models.routes import api
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
import os

def create_app(config_name='development'):
    app = Flask(__name__)
    # app.config.from_object(config[config_name])
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig) 

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ajali_user:aJali!@db:5432/ajali_db'
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