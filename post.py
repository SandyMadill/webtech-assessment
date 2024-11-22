import datetime
from crypt import methods

from flask import Blueprint, render_template, session

from database import get_db
from user import User, checkSession

postApi = Blueprint('post-api', __name__, template_folder='templates')

class Post:
    def __init__(self, postId, userId, postText, hasImages, dateAndTime, replyId, repostId):
        self.postId = postId
        self.userId = userId
        self.postText = postText
        self.hasImages = hasImages
        self.replyId = replyId
        self.dateAndTime = dateAndTime
        self.repostId = repostId


@postApi.route("/post/<postId>/")
def post(postId=None):
    db = get_db()
    for p in db.cursor().execute("SELECT * FROM Post WHERE post_id=?", [postId]):
        post = Post(p[0],p[1],p[2],p[3],p[5],None,None)
        for u in db.cursor().execute("SELECT * FROM User WHERE user_id=?", [str(post.userId)]):
            user = User(u[0], u[1], u[3], u[4])
            return render_template("post.html", post=post, user=user)
        print("id: " + str(post.userId) + " userId: " + str(post.postId) + " text: " + post.postText + " image: " + str(post.hasImages) + " date: " +str(post.dateAndTime))
    return "Post Does Not Exist"

@postApi.route('/post/like/<postId>/')
def getLikes(postId=None):
    db = get_db()
    sql = db.cursor().execute("SELECT user_id FROM Likes WHERE post_id=?", [postId])
    likes = []
    for like in sql:
        likes.append(like[0])

    return likes

@postApi.route('/post/like/button/<postId>/', methods=["GET"])
def getLikeButton(postId=None):
    if checkSession():
        db = get_db()
        if (likesPost(postId)):
            return render_template("unlike-button.html")
        else:
            return render_template("like-button.html")

@postApi.route('/post/like/<postId>/', methods=["POST"])
def likePost(postId=None):
    if checkSession():
        db = get_db()
        if likesPost(postId) == False:
            db.cursor().execute("INSERT INTO Likes(post_id, user_id) VALUES(?,?)", (postId, session['id']))
            db.commit()
            return getLikeButton(postId)
        else:
            return "null"
    else:
        return "null"

@postApi.route('/post/like/<postId>/', methods=["DELETE"])
def unlikePost(postId=None):
    if checkSession():
        db = get_db()
        if likesPost(postId):
            db.cursor().execute("DELETE FROM Likes WHERE post_id=? AND user_id=?", (postId, session['id']))
            db.commit()

            return getLikeButton(postId)
        else:
            return "null"
    else:
        return "null"

@postApi.route('/post/repost/<postId>/')
def getReposts(postId=None):
    db = get_db()
    sql = db.cursor().execute("SELECT user_id FROM Post WHERE repost_id=?", [postId])
    reposts = []
    for repost in sql:
        reposts.append(repost[0])
    return reposts

@postApi.route('/post/repost/button/<postId>/', methods=["GET"])
def getRepostButton(postId=None):
    if checkSession():
        db = get_db()
        sql = db.cursor().execute("SELECT * FROM User")
        if (repostedPost(postId)):
            return render_template("unrepost-button.html")
        else:
            return render_template("repost-button.html")

@postApi.route('/post/repost/<postId>/', methods=["POST"])
def repost(postId=None):
    if checkSession():
        db = get_db()
        if repostedPost(postId) == False:
            db.cursor().execute("INSERT INTO Post(repost_id, user_id, date_and_time) VALUES(?,?,?)", (postId, session['id'], datetime.datetime.now()))
            db.commit()
            return getRepostButton(postId)
        else:
            return "null"
    else:
        return "null"

@postApi.route('/post/repost/<postId>/', methods=["DELETE"])
def unrepost(postId=None):
    if checkSession():
        db = get_db()
        if repostedPost(postId):
            db.cursor().execute("DELETE FROM Post WHERE repost_id=? AND user_id=?", (postId, session['id']))
            db.commit()
            return getRepostButton(postId)
        else:
            return "null"
    else:
        return "null"

def likesPost(postId):
    db = get_db()
    sql = db.cursor().execute("SELECT user_id FROM Likes WHERE post_id=? AND user_id=?", (postId, session['id']))
    for a in sql:
        return True
    return False

def repostedPost(postId):
    db = get_db()
    sql = db.cursor().execute("SELECT user_id FROM Post WHERE repost_id=? AND user_id=?", (postId, session['id']))
    for a in sql:
        return True
    return False

