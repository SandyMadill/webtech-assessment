import base64
import datetime
import os
import pathlib
from crypt import methods

import flask
from flask import Blueprint, render_template, session, request
from rpm import file

from database import get_db
from follow import isFollowing
from notifications import makeNotification, deleteNotification
from user import User, checkSession, getUserFromSql, getUser
from usersession import getSession

postApi = Blueprint('post-api', __name__, template_folder='templates')

# contains the necessary properties of a post
class Post:
    def __init__(self, postId, userId, postText, hasImages, dateAndTime, replyId, repostId):
        self.postId = postId
        self.userId = userId
        self.postText = postText
        self.hasImages = hasImages
        self.replyId = replyId
        self.dateAndTime = dateAndTime
        self.repostId = repostId
        self.likeCount = len(getLikes(postId))
        self.repostCount = len(getReposts(postId))
        self.likesPost = None                       #   contains if the logged in user has liked the post
        self.repostedPost = None                    #   contains if the logged in user has reposted the post
        if (checkSession()):
            self.likesPost = likesPost(postId)
            self.repostedPost = repostedPost(postId)


#converts a basic select * from post sql statement and converts it into an instance of the post object
def getPostFromSql(sql):
    for p in sql:
        post = Post(p[0], p[1], p[2], p[3], p[5], p[6], p[4])
        db = get_db()
        if post.repostId == None:
            return post
        else:
            rpsql = db.cursor().execute("SELECT * FROM Post p INNER JOIN User u ON p.user_id = u.user_id WHERE post_id=? AND BANNED=FALSE", [post.repostId])
            for rp in rpsql:
                repost = Post(rp[0], rp[1], rp[2], rp[3], rp[5], rp[6], post.userId)
                return repost
    return None

#returns the post as a post object
def getPostById(postId):
    db = get_db()
    return getPostFromSql(db.cursor().execute("SELECT * FROM Post p INNER JOIN User u ON p.user_id = u.user_id WHERE post_id=? AND BANNED=FALSE", [postId]))


def getPost(postId=None):
    db = get_db()
    post = getPostFromSql(db.cursor().execute("SELECT * FROM Post p INNER JOIN User u ON p.user_id = u.user_id WHERE post_id=? AND BANNED=FALSE", [postId]))

    if (post == None):
        return None
    elif (post.repostId == None):
        user = getUser(post.userId)
        return render_template("post.html", post=post, user=user, rpUser=None, userSession=getSession(), following = isFollowing(post.userId))
    else:
        user = getUser(post.userId)
        rpUser = getUser(post.repostId)
        return render_template("post.html", post=post, user=user, rpUser=rpUser, userSession=getSession(), following = isFollowing(post.userId))

# Will get the post from the id in the perameter, then if the post retrieved has a reply id it will retrieve the post that the replid belongs to
# this process will repeat untill it retrieves a post that does not have a reply id
# will return an array containing every post rendered with the post.html template
@postApi.route('/post/thread/<postId>/')
def getThread(postId=None):
    # get the selected post
    db = get_db()
    post = getPostFromSql(db.cursor().execute("SELECT * FROM Post p INNER JOIN User u ON p.user_id = u.user_id WHERE post_id=? AND BANNED=FALSE", [postId]))

    # if this post is not a reply then return a tuple containing the post id and the rendered post
    # if the post is a reply then return it with an array containing the other posts in the thread before it
    if post == None:
        return []
    elif post.replyId == None:
        return [[post.postId, getPost(post.postId)]]
    else:
        threadArray = getThread(post.replyId)
        threadArray.append([post.postId, getPost(post.postId)])
        return threadArray

@postApi.route("/create-post/", methods=['POST','GET'])
def createPost():
    if (checkSession()):
        db = get_db()
        if (request.method == 'POST'):
            userId = session['id']
            try:
                replyId = request.form['replyId']
            except:
                replyId = None
            text = request.form['text']
            sql = db.cursor().execute("INSERT INTO Post(user_id, post_text, has_images, date_and_time, reply_id) VALUES(?,?,false,?,?) RETURNING post_id as post_id", (userId, text, datetime.datetime.now(), replyId)).fetchone()
            db.commit()
            if (replyId != None):
                for s in sql:
                    postId = s
                    makeNotification(getPostById(replyId).userId, int(session['id']), postId, "reply")

            return "posted successfully"
    else:
        return ""

@postApi.route("/create-post/img/", methods=['POST'])
def createPostImg():
    if (checkSession()):
        db = get_db()
        userId = session['id']
        try:
            replyId = request.form['replyId']
        except:
            replyId = None
        text = request.form['post-text']
        sql = db.cursor().execute("INSERT INTO Post(user_id, post_text, has_images, date_and_time, reply_id) VALUES(?,?,true,?,?) RETURNING post_id as post_id", (userId, text, datetime.datetime.now(), replyId)).fetchone()
        db.commit()

        for s in sql:
            postId = s
            if (replyId != None):
                makeNotification(getPostById(replyId).userId, int(session['id']), postId, "reply")

        image = request.files['uploadImage']
        fileType = (pathlib.Path(image.filename).suffix)
        if fileType == '.jpeg' or fileType == '.jpg' or fileType == '.png':
            os.mkdir('./static/img/post-img/'+str(postId))
            image.save('./static/img/post-img/'+str(postId)+'/img.jpg')
        return "posted successfully"

@postApi.route("/post/<postId>/")
def renderPost(postId=None):
    db = get_db()
    post = getPostFromSql(db.cursor().execute("SELECT * FROM Post p INNER JOIN User u ON p.user_id = u.user_id WHERE post_id=? AND BANNED=FALSE", [postId]))
    if (post.repostId == None):
        user = getUser(post.userId)
        return render_template("index.html", page="post", post=post, user=user, rpUser=None, userSession=getSession(), following = isFollowing(post.userId))
    else:
        user = getUser(post.userId)
        rpUser = getUser(post.repostId)
        return render_template("index.html", page="post", post=post, user=user, rpUser=rpUser, userSession=getSession(), following = isFollowing(post.userId))


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
        db= get_db()
        post = getPostFromSql(db.cursor().execute("SELECT * FROM Post p INNER JOIN User u ON p.user_id = u.user_id WHERE post_id=? AND BANNED=FALSE", [postId]))
        if (likesPost(postId)):
            return render_template("unlike-button.html", post=post)
        else:
            return render_template("like-button.html", post=post)

@postApi.route('/post/like/<postId>/', methods=["POST"])
def likePost(postId=None):
    if checkSession():
        db = get_db()
        if likesPost(postId) == False:
            db.cursor().execute("INSERT INTO Likes(post_id, user_id) VALUES(?,?)", (postId, session['id'],))
            db.commit()

            makeNotification(getPostById(postId).userId, int(session['id']), postId, "like")

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
            db.cursor().execute("DELETE FROM Likes WHERE post_id=? AND user_id=?", (postId, session['id'],))
            db.commit()

            deleteNotification(getPostById(postId).userId, int(session['id']), postId, "like")

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
        post = getPostFromSql(db.cursor().execute("SELECT * FROM Post WHERE post_id=?", [postId]))
        db.commit()
        if (repostedPost(postId)):
            return render_template("unrepost-button.html", post=post)
        else:
            return render_template("repost-button.html", post=post)

@postApi.route('/post/repost/<postId>/', methods=["POST"])
def repost(postId=None):
    if checkSession():
        db = get_db()
        if repostedPost(postId) == False:
            db.cursor().execute("INSERT INTO Post(repost_id, user_id, date_and_time) VALUES(?,?,?)", (postId, session['id'], datetime.datetime.now()))
            db.commit()

            makeNotification(getPostById(postId).userId, int(session['id']), postId, "repost")

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
            db.cursor().execute("DELETE FROM Post WHERE repost_id=? AND user_id=?", (postId, session['id'],))
            db.commit()

            deleteNotification(getPostById(postId).userId, int(session['id']), postId, "repost")

            return getRepostButton(postId)
        else:
            return "null"
    else:
        return "null"

def likesPost(postId):
    db = get_db()
    sql = db.cursor().execute("SELECT user_id FROM Likes WHERE post_id=? AND user_id=?", (postId, session['id'],))
    for a in sql:
        return True
    return False

def repostedPost(postId):
    db = get_db()
    sql = db.cursor().execute("SELECT user_id FROM Post WHERE repost_id=? AND user_id=?", (postId, session['id'],))
    for a in sql:
        return True
    return False

