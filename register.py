from flask import Flask, render_template, request, Blueprint
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

            print(passHash)
            print(passHash == bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))




            db.cursor().execute("INSERT INTO User(username, password, display_name, role, banned) VALUES(?,?,?,'user',false)", (username, passHash, displayName));

            db.commit();
        return render_template('register.html')
    else:
        return "Already Logged In"
