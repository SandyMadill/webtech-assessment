from flask import Flask, render_template, request, Blueprint, redirect
from database import get_db
import bcrypt

from user import checkSession

registerApi = Blueprint('register-api', __name__, template_folder='templates')

@registerApi.route("/register/", methods=['POST', 'GET'])
def initReg():
    if checkSession() == False:

        db = get_db()
        if request.method == 'POST':
            print (request.form)
            username = request.form['username']
            displayName = request.form['displayName']
            password = request.form['password']

            passHash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())



            try:
                db.cursor().execute("INSERT INTO User(username, password, display_name, role, banned) VALUES(?,?,?,'user',false)", (username, passHash, displayName));
                db.commit();
            except Exception as e:
                db.commit()
                raise Exception("Username already taken")
            return redirect('/login/')
        return render_template('index.html', page="register", pageTitle="register", userSession=None)
    else:
        return redirect('/feed/')
