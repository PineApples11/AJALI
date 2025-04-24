import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv
from models import db, TokenBlocklist
from routes import api

load_dotenv()  # Load environment variables from .env

def create_app():
    app = Flask(__name__)
    CORS(app)

    # --- CONFIG ---
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:5432/ajali_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')  # Change this in production!
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    # --- INIT EXTENSIONS ---
    db.init_app(app)
    Migrate(app, db)
    jwt = JWTManager(app)

    # --- JWT CALLBACKS ---
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(msg="Token has been revoked"), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(msg="Token has expired"), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(msg="Invalid token"), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(msg="Missing token"), 401

    # --- ROUTES ---
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def home():
        return jsonify({"message": "AJALI API is running 🚨"}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
