from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db, User, Admin, IncidentReport, Media, TokenBlocklist
from flask_cors import CORS
from routes import api  # CRUD routes will be in routes.py

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in prod!
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    # Initialize Extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Register blueprint
    app.register_blueprint(api, url_prefix='/api')

    # Token revocation check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    # Handle revoked token
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(msg="Token has been revoked"), 401

    # Handle expired token
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(msg="Token has expired"), 401

    # Handle invalid token
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(msg="Invalid token"), 422

    # Handle missing token
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(msg="Missing token"), 401

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the AJALI API"}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
