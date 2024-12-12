from flask import Flask, session, redirect, send_from_directory

from config import getKey
from report import reportApi
from follow import followApi
from login import loginApi
from notifications import notificationApi
from post import postApi
from postlist import postListApi
from register import registerApi
from settings import settingsApi
from usersession import getSession
import os

app = Flask(__name__)
app.secret_key = getKey()


@app.context_processor
def handle_context():
    return dict(os=os)
app.register_blueprint(postApi)
app.register_blueprint(followApi)
app.register_blueprint(loginApi)
app.register_blueprint(registerApi)
app.register_blueprint(postListApi)
app.register_blueprint(notificationApi)
app.register_blueprint(reportApi)
app.register_blueprint(settingsApi)

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