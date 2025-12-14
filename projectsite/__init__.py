import os
from . import db
from flask import Flask
from .views import indexBp, blogBP
from .api import apiBp
from .auth import authBp
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
            MYSQL_HOST=os.environ.get("MYSQL_HOST", "localhost"),
            MYSQL_USER=os.environ.get("MYSQL_USER", "root"),
            MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD", "root"),
            MYSQL_DB=os.environ.get("MYSQL_DB", "psu"),
            MYSQL_CURSORCLASS=os.environ.get("MYSQL_CURSORCLASS", "DictCursor"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", "super-secret-key"),
        )
    
    else:
        app.config.from_mapping(test_config)
    
    db.init_app(app)
    JWTManager(app)


    app.register_blueprint(indexBp)
    app.register_blueprint(blogBP)
    app.register_blueprint(apiBp)
    app.register_blueprint(authBp)

    return app