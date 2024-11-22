from flask import Blueprint, render_template, session, request
from database import get_db
from user import checkSession

followApi = Blueprint('follow-api', __name__, template_folder='templates')
@followApi.route('/follow/<followeeId>')
def init_follow(followeeId=None):
    if (checkSession()):
        if (followeeId != session['id']):
            return render_template("follow.html", userId=followeeId)
        else:
            return "null"
    else:
        return "null"
@followApi.route('/follow/<followeeId>/', methods=["POST"])
def followUser(followeeId=None):
    if (checkSession()):
        if (isFollowing(followeeId) == False and followeeId != session['id']):
            db=get_db()
            db.cursor().execute("INSERT INTO Follow(follower_id, followee_id) VALUES(?,?)", (session['id'], followeeId))
            db.commit()
            return getFollowButton(followeeId)
        else:
            return "null"
    return "null"

@followApi.route('/follow/<followeeId>/', methods=["DELETE"])
def unfollowUser(followeeId=None):
    if (checkSession()):
        if (isFollowing(followeeId) and followeeId != session['id']):
            db=get_db()
            db.cursor().execute("DELETE FROM Follow WHERE follower_id=? AND followee_id=?", (session['id'], followeeId))
            db.commit()
            return getFollowButton(followeeId)
        else:
            return "null"
    return "null"
@followApi.route('/follow/button/<followeeId>/', methods=["GET"])
def getFollowButton(followeeId=None):
    if (checkSession()):
        if (followeeId != session['id']):
           db = get_db()
           if isFollowing(followeeId):
               return render_template("unfollowbutton.html",userId=followeeId)
           else:
               return render_template("followbutton.html", userId=followeeId)
        else:
            return "null"
    else:
        return "null"

def isFollowing(followeeId):
    db = get_db()
    for row in db.cursor().execute("SELECT * FROM Follow WHERE follower_id=? AND followee_id=?",(session["id"], followeeId)):
        return True
    return False