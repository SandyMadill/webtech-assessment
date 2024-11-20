from flask import render_template, request, session
from database import get_db
import bcrypt

def initLogin():
    try:
        if (session['id']):
            return "Already Logged in"
    except KeyError:
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
        return render_template('login.html')