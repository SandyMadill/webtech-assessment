from flask import Flask, g, session, render_template
import os
import sqlite3

from samba.dcerpc.drsblobs import replUpToDateVectorCtr

from register import initReg
from database import get_db
from login import initLogin
from createpost import initCreatePost
from user import User
from post import Post
from follow import follow

app = Flask(__name__)
app.secret_key = 'fkgjdflg£$5;"!4$^&RTH42£$%'
app.register_blueprint(follow)

@app.route("/")
def root():
    users = []
    db = get_db();
    for row in db.cursor().execute("SELECT rowid, * FROM Post"):
        print(row)
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

@app.route("/create-post/", methods=['POST','GET'])
def createPost():
    return initCreatePost()

@app.route("/post/<postId>")
def post(postId=None):
    db = get_db()
    for p in db.cursor().execute("SELECT * FROM Post WHERE post_id=?", [postId]):
        post = Post(p[0],p[1],p[2],p[3],p[5],None,None)
        for u in db.cursor().execute("SELECT * FROM User WHERE user_id=?", [str(post.userId)]):
            user = User(u[0], u[1], u[3], u[4])
            return render_template("post.html", post=post, user=user)
        print("id: " + str(post.userId) + " userId: " + str(post.postId) + " text: " + post.postText + " image: " + str(post.hasImages) + " date: " +str(post.dateAndTime))
    return "aaaaaaaaaa"

@app.route("/sql/<stmt>")
def sql(stmt=None):
    db = get_db()

    for row in db.cursor().execute("select * from Follow"):
        print(str(row))
    return "Aaaaa"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
