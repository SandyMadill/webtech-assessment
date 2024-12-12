import bcrypt
from flask import Flask, g
import os
import sqlite3

from config import getKey

app = Flask(__name__)
db_location = 'db/GreenGround.db'
app.secret_key = getKey()

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db(modName, modDisplayname, modPassword):
    with app.app_context():
        db = get_db()
        with app.open_resource('db/schema.sql', mode='r') as f:db.cursor().executescript(f.read())
        db.commit()
        passHash = bcrypt.hashpw(modPassword.encode('utf-8'), bcrypt.gensalt())

        db.cursor().execute("INSERT INTO User(username, password, display_name, role, banned) VALUES(?,?,?,'mod',false)",(modName, passHash, modDisplayname,))
        db.commit()
        print("DATABASE INITIALIZED")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


