from flask import Flask, session, render_template, Blueprint

from createpost import initCreatePost, createPostApi
from database import get_db
from follow import followApi
from login import initLogin
from post import Post, postApi
from register import initReg
from user import User
app = Flask(__name__)
app.secret_key = 'fkgjdflg£$5;"!4$^&RTH42£$%'

app.register_blueprint(postApi)
app.register_blueprint(followApi)
app.register_blueprint(createPostApi)

@app.route("/")
def root():
    users = []
    db = get_db();
    for row in db.cursor().execute("SELECT rowid, * FROM Post"):
        users.append(str(row))
    return users


@app.route("/register/", methods=['POST', 'GET'])
def reg():
    return initReg()

@app.route("/login", methods=['POST','GET'])
def login():
    return initLogin()

@app.route("/logout")
def logout():
    session.pop('id', None)
    session.pop('role', None)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
