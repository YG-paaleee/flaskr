from flask_mysqldb import MySQL
from flask import g, current_app
import click

mysql = MySQL()

def get_db():
    if "db" not in g:
        g.db = mysql.connection
    return g.db

def close_db(e=None):
    g.pop("db", None)

def init_db():
    conn = get_db()
    
    with current_app.open_resource("badangDB.sql") as f:
        sql_commands = f.read().decode("utf8")

    with conn.cursor() as cur:
        for stmt in sql_commands.split(";"):
            stmt = stmt.strip()
            
            if stmt:
                cur.execute(stmt)

    conn.commit()
    click.echo("Initialized database.")

@click.command("init-db")
def init_db_command():
    init_db()

def init_app(app):
    mysql.init_app(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)