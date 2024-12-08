from flask import render_template, request, session, Blueprint
from database import get_db
import datetime

from usersession import getSession, checkSession

createPostApi = Blueprint('create-post-api', __name__, template_folder='templates')

@createPostApi.route("/create-post/", methods=['POST','GET'])
def initCreatePost():
    if (checkSession()):
        db = get_db()
        if (request.method == 'POST'):
            userId = session['id']
            replyId = None
            if (request.form['replyId'] != None):
                replyId = request.form['replyId']
            text = request.form['text']
            db.cursor().execute("INSERT INTO Post(user_id, post_text, has_images, date_and_time, reply_id) VALUES(?,?,false,?,?)", (userId, text, datetime.datetime.now(), replyId));
            db.commit()
            return "posted successfully"
    else:
        return ""
