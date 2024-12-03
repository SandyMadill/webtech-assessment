from flask import Flask, session, render_template, Blueprint, redirect

from createpost import initCreatePost, createPostApi
from database import get_db
from follow import followApi
from login import initLogin, loginApi
from post import Post, postApi
from postlist import postListApi
from register import initReg, registerApi
from usersession import getSession

app = Flask(__name__)
app.secret_key = 'fkgjdflg£$5;"!4$^&RTH42£$%'

app.register_blueprint(postApi)
app.register_blueprint(followApi)
app.register_blueprint(createPostApi)
app.register_blueprint(loginApi)
app.register_blueprint(registerApi)
app.register_blueprint(postListApi)

@app.route("/")
def root():
    if (getSession() != None):
        return redirect('feed')
    else:
        return redirect('discover')

@app.route("/logout/")
def logout():
    session.pop('id', None)
    session.pop('role', None)
    return redirect('/login/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
