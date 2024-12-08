from flask import Flask, session, redirect, send_from_directory
from createpost import createPostApi
from follow import followApi
from login import loginApi
from post import postApi
from postlist import postListApi
from register import registerApi
from images import imageApi
from usersession import getSession
import os

app = Flask(__name__)
app.secret_key = 'fkgjdflg£$5;"!4$^&RTH42£$%'


@app.context_processor
def handle_context():
    return dict(os=os)
app.register_blueprint(postApi)
app.register_blueprint(followApi)
app.register_blueprint(createPostApi)
app.register_blueprint(loginApi)
app.register_blueprint(registerApi)
app.register_blueprint(postListApi)
app.register_blueprint(imageApi)

@app.route("/")
def root():
    if (getSession() != None):
        return redirect('/feed/')
    else:
        return redirect('/discover/')

@app.route("/logout/")
def logout():
    session.pop('id', None)
    session.pop('role', None)
    return redirect('/login/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)