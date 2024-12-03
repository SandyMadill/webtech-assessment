from flask import render_template, request, session, Blueprint
from database import get_db
import bcrypt

from user import checkSession

loginApi = Blueprint('login-api', __name__, template_folder='templates')

@loginApi.route("/login/", methods=['POST','GET'])
def initLogin():
    if checkSession() == False:
        db = get_db()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            sql = db.cursor().execute("SELECT user_id, username, password, role FROM User WHERE username=?", [username])

            for row in sql:
                if (row[2] == bcrypt.hashpw(password.encode('utf-8'), row[2])):

                    session['id'] = str(row[0])
                    session['role'] = str(row[3])
                    print(session['id'])
        return render_template('index.html', page='login', pageTitle='Login')
    else:
        return "Already Logged In"