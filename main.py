from flask import Flask, g, session
import os
import sqlite3
from register import initReg
from database import get_db
from login import initLogin

app = Flask(__name__)
app.secret_key = 'fkgjdflg£$5;"!4$^&RTH42£$%'


@app.route("/")
def root():
    users = []
    db = get_db();
    for row in db.cursor().execute("SELECT rowid, * FROM User"):
        print(row)
        users.append(str(row))
    return users


@app.route("/register/", methods=['POST', 'GET'])
def reg():
    return initReg()

@app.route("/login", methods=['POST','GET'])
def login():
    return initLogin()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
