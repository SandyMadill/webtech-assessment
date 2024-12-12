from datetime import datetime, date

from flask import render_template, request, session, Blueprint, redirect
from orca.braille import resetFlashTimer

from database import get_db
import bcrypt

from user import checkSession
from usersession import getSession

loginApi = Blueprint('login-api', __name__, template_folder='templates')

@loginApi.route("/login/", methods=['POST','GET'])
def initLogin():
    if checkSession() == False:
        db = get_db()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            sql = db.cursor().execute("SELECT user_id, username, password, role, banned, unban_date FROM User WHERE username=?", [username])

            for row in sql:
                if (row[2] == bcrypt.hashpw(password.encode('utf-8'), row[2])):
                    if bool(row[4]) == True:
                        if row[5] == None:
                            return render_template('index.html', page='login', pageTitle='Login', banned=True, unbanDate=None, userSession=None)
                        else:
                            unbanDate = date.fromisoformat(row[5])
                            if unbanDate > date.today():
                                return render_template('index.html', page='login', pageTitle='Login', banned=True, unbanDate=unbanDate, userSession=None)
                            else:
                                db.cursor().execute("UPDATE User SET banned = FALSE AND unban_date=NULL where username=?", [username])
                                db.commit()
                                session['id'] = str(row[0])
                                session['role'] = str(row[3])
                                return redirect('/feed/')
                    else:
                        session['id'] = str(row[0])
                        session['role'] = str(row[3])
                        return redirect('/feed/')
        return render_template('index.html', page='login', pageTitle='Login', userSession=None, banned=False, unbanDate=None)
    else:
        return redirect('/feed/')