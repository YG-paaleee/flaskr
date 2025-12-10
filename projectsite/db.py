from flask_mysqldb import MySQL
from flask import g

mysql = MySQL()

def get_db():
    if "db" not in g:
        g.db = mysql.connection
    return g.db

def close_db(e=None):
    g.pop("db", None)
def init_app(app):
    mysql.init_app(app)
    app.teardown_appcontext(close_db)