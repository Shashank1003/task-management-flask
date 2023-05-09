from flask import Flask, jsonify
from flask_smorest import Api
from resources.task import blp as TaskBlueprint
from resources.subTask import blp as SubTaskBlueprint
from resources.user import blp as UserBlueprint
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from datetime import timedelta

from db import db
import os
import models
from blocklist import BLOCKLIST


def create_app():
    app = Flask(__name__)

    # app.config["PROPAGATE_EXCEPTIONS"] = True
    # app.config["API_TITLE"] = "task-management REST API"
    # app.config["API_VERSION"] = "v1"
    # app.config["OPENAPI_VERSION"] = "3.0.3"
    # app.config["OPENAPI_URL_PREFIX"] = "/"
    # app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # app.config[
    #     "OPENAPI_SWAGGER_UI_URL"
    # ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://mdmbfkpf:YIeX0Tvh3Thp8GdBl7OCQGCw1xOt71dh@tiny.db.elephantsql.com/mdmbfkpf"
    # app.config[
    # "SQLALCHEMY_DATABASE_URI"
    # ] = "postgresql://zoro:zoro113@localhost/TaskManagement"
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    migrate = Migrate(app, db)

    # api = Api(app)
    app.config["JWT_SECRET_KEY"] = "244628952963955921591023472340882159530"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request doesnot contain an access token",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # @app._got_first_request
    # def createTables():
    #     db.create_all()

    app.register_blueprint(TaskBlueprint)
    app.register_blueprint(SubTaskBlueprint)
    app.register_blueprint(UserBlueprint)

    return app
