from flask import Flask, render_template, request
from database import get_db
import bcrypt

def initReg():
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
