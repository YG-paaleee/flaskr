import os
from flask import Flask
from .views import indexBp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        MYSQL_HOST="localhost",
        MYSQL_USER="root",
        MYSQL_PASSWORD="root",
        MYSQL_DB="psu",
        MYSQL_CURSORCLASS="DictCursor",
      )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(indexBp)

    return app