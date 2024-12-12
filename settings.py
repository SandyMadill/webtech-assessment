import io
import os
import pathlib
from PIL import Image

from flask import Blueprint, render_template, request

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
        return "posted successfully"