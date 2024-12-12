import io
import os
import pathlib

import bcrypt
from PIL import Image

from flask import Blueprint, render_template, request

from database import get_db
from user import checkSession, getUser
from usersession import getSession

settingsApi = Blueprint('settings-api', __name__, template_folder='templates')

@settingsApi.route('/settings/', methods=['GET'])
def getSettings():
    if checkSession():
        user = getUser(getSession().user_id)
        return render_template('index.html', page='settings', userSession=getSession(), user=user)

@settingsApi.route('/settings/pfp/', methods=['PUT'])
def updatePfp():
    if checkSession():
        userSession = getSession()
        image = Image.open(request.files['uploadImage'], mode='r')
        l = image.resize((400, 400), Image.Resampling.LANCZOS)
        s = image.resize((40, 40), Image.Resampling.LANCZOS)
        os.mkdir('./static/img/pfp/' + str(userSession.user_id))
        l.save('./static/img/pfp/'+str(userSession.user_id)+'/400x400.jpg/')
        s.save('./static/img/pfp/' + str(userSession.user_id) + '/40x40.jpg/')
        return "image uploaded"

@settingsApi.route('/settings/username/', methods=['PUT'])
def updateUsername():
    if checkSession():
        userSession = getSession()
        username = request.form.get('username')
        db = get_db()
        print(userSession.user_id)
        try:
            db.cursor().execute("UPDATE User SET username = ? WHERE user_id = ?", (username, userSession.user_id, ))
            db.commit()
        except Exception as e:
            db.commit()
            raise Exception("Username already taken")
        return username

@settingsApi.route('/settings/display-name/', methods=['PUT'])
def updateDisplayName():
    if checkSession():
        userSession = getSession()
        displayname = request.form.get('displayname')
        db = get_db()
        print(userSession.user_id)
        try:
            db.cursor().execute("UPDATE User SET display_name = ? WHERE user_id = ?", (displayname, userSession.user_id, ))
            db.commit()
        except Exception as e:
            db.commit()
            raise Exception(e)
        return displayname

@settingsApi.route('/settings/password/', methods=['PUT'])
def updatePassword():
    if checkSession():
        userSession = getSession()
        oldPassword = request.form.get('old-password')

        db = get_db()
        print(userSession.user_id)
        try:
            sql = db.cursor().execute("SELECT password FROM User WHERE user_id=?", (userSession.user_id,))
            for row in sql:
                if (row[0] == bcrypt.hashpw(oldPassword.encode('utf-8'), row[0])):
                    newPassword = request.form.get('password')
                    passHash = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
                    db.cursor().execute("UPDATE User SET password = ? WHERE user_id = ?", (passHash, userSession.user_id,))
                    db.commit()
                else:
                    raise Exception("Wrong password")
        except Exception as e:
            db.commit()
            raise Exception(e)
        return "password changed"