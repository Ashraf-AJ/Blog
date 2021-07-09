from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from dotenv import load_dotenv
from api.cache import Cache
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cache = Cache()


def create_app(config_name):
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    from .graphql import graphql as graphql_blueprint

    app.register_blueprint(graphql_blueprint)

    return app
