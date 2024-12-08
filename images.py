from os import sendfile

from flask import Blueprint, send_from_directory
from werkzeug.utils import send_file

imageApi = Blueprint('img-api', __name__, template_folder='templates')

@imageApi.route('/img/pfp/<userId>/<scale>/')
def getPfp(userId = None, scale = None):
    if (scale == "large"):
        path = '/img/pfp/' + str(userId) + '/400x400.jpg'
        return send_from_directory(imageApi.static_folder, ('img/pfp/'+str(userId)+'/400x400.jpg'))

    elif (scale == "small"):
        try:
            path = '/img/pfp/' + str(userId) + '/40x40.jpg'
            print(path)
            return send_from_directory(imageApi.static_folder, path)
        except TypeError:
            return send_from_directory(imageApi.static_folder, '/img/pfp/default/40x40.jpg')
    else:
        return None