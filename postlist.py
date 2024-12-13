import datetime
import json

from Xlib.ext.randr import PROPERTY_CLONE_LIST
from click import DateTime
from flask import Flask, Blueprint, render_template, logging, request, redirect

from database import get_db
from follow import getFolloweeIdsForUser
from post import getPostFromSql, getPost
from user import getUser, checkSession
from usersession import getSession

postListApi = Blueprint('post-list-api', __name__, template_folder='templates')

@postListApi.route('/feed/', methods=['GET'])
def getFeed():
    if checkSession():
        followees = getFolloweeIdsForUser()
        if len(followees)==0:
            return render_template("index.html", page="feed", posts=[], lastDate=datetime.datetime.now(), userSession = getSession(), where=[])
        where = []
        for followee in followees:
            where.append(["user_id",followee])
        posts = (getPostList(where,"desc", str(datetime.datetime.now())))
        return render_template("index.html", page="feed", posts=posts[0], lastDate=posts[1], userSession = getSession(), where=where)
    else:
        return redirect('/discover/')
@postListApi.route('/discover/', methods=['GET'])
def getDiscoverFeed():
    posts = getPostList([],"desc",str(datetime.datetime.now()))
    return render_template("index.html", page="feed", posts=posts[0], lastDate=posts[1], userSession = getSession(), where=[])

@postListApi.route('/profile/<userId>/', methods=['GET'])
def getProfile(userId=None):
    posts = getPostList([["user_id",userId]],"desc",str(datetime.datetime.now()))
    user = getUser(userId)
    return render_template("index.html", page="profile", posts=posts[0], lastDate=posts[1], user=user, userSession=getSession(), where=[["user_id",userId]])


@postListApi.route('/replies/<postId>/', methods=['GET'])
def getReplies(postId=None):
    return getPostList([["reply_id",postId]],"desc",str(datetime.datetime.now()))



@postListApi.route('/post-list/<where>/<ord>/<afterDate>/', methods=['GET'])
def recievePostListRequest(where = None, ord = None, afterDate = None):
    return getPostList(json.loads(where),ord,afterDate)

def getPostList(where = None, ord = None, afterDate = None):
    db = get_db()
    posts = []
    args = []
    lastDate = None
    stmt = "SELECT p.post_id, p.date_and_time FROM Post p INNER JOIN User u ON p.user_id = u.user_id WHERE "
    if len(where) > 0:
        stmt += "("
    for i in range(len(where)):
        stmt+= "p." + where[i][0] + "=? "
        args.append(where[i][1])
        if(i+1 < len(where)):
            stmt += "OR "

    if len(where) > 0:
        stmt += ") AND "

    if (ord == "desc"):
        stmt += "p.date_and_time < ? AND BANNED=FALSE ORDER BY p.date_and_time DESC LIMIT 10"
    else:
        stmt += "p.date_and_time > ? AND BANNED=FALSE ORDER BY p.date_and_time ASC LIMIT 10"
    args.append(afterDate)
    print(stmt)
    for p in db.cursor().execute(stmt, args):
        post = getPost(p[0])
        if post != None:
            posts.append([p[0],post])
            lastDate=p[1]
    return [posts, lastDate]