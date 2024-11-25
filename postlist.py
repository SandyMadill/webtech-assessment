import datetime
from Xlib.ext.randr import PROPERTY_CLONE_LIST
from click import DateTime
from flask import Flask, Blueprint, render_template

from config import config
from database import get_db
from post import getPostFromSql, getPost

postListApi = Blueprint('post-list-api', __name__, template_folder='templates')

@postListApi.route('/post-list/', methods=['GET'])
def getPostList():
    db = get_db()
    posts = []
    i = 0;
    LastDate=None
    for p in db.cursor().execute("SELECT post_id, date_and_time FROM Post ORDER BY date_and_time DESC LIMIT 10"):
        posts.append(getPost(p[0]))
        lastDate=p[1]
        i+=1
        print(i)
        print(lastDate)
    return render_template('post-list.html', posts=posts, lastDate=lastDate)

@postListApi.route('/post-list/<afterDate>/<ord>', methods=['GET'])
def getPostListWithDate(afterDate = None, ord = None):
    if (ord == "desc"):
        db = get_db()
        posts = []

        lastDate=None
        for p in db.cursor().execute("SELECT post_id, date_and_time FROM Post WHERE date_and_time < ? ORDER BY date_and_time DESC LIMIT 10", [afterDate]):
            posts.append(getPost(p[0]))
            lastDate=p[1]
        return [posts, lastDate]
    else:
        db = get_db()
        posts = []
        LastDate = None
        for p in db.cursor().execute("SELECT post_id, date_and_time FROM Post WHERE date_and_time > ? ORDER BY date_and_time ASC LIMIT 10", [afterDate]):
            posts.append(getPost(p[0]))
            lastDate = p[1]
        return [posts]
