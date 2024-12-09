from flask import Blueprint, render_template, session, request

from database import get_db
from notifications import makeNotification, deleteNotification
from user import checkSession, getUserFromSql

followApi = Blueprint('follow-api', __name__, template_folder='templates')
@followApi.route('/follow/<followeeId>')
def init_follow(followeeId=None):
    if (checkSession()):
        if (followeeId != session['id']):
            return render_template("follow.html", userId=followeeId)
        else:
            return ""
    else:
        return ""
@followApi.route('/follow/<followeeId>/', methods=["POST"])
def followUser(followeeId=None):
    if (checkSession()):
        if (isFollowing(followeeId) == False and followeeId != session['id']):
            db=get_db()
            db.cursor().execute("INSERT INTO Follow(follower_id, followee_id) VALUES(?,?)", ([session['id']], followeeId))
            db.commit()

            makeNotification(followeeId, int(session['id']), None, "follow")

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

            deleteNotification(followeeId, int(session['id']), None, "follow")

            return getFollowButton(followeeId)
        else:
            return "null"
    return "null"
@followApi.route('/follow/button/<followeeId>/', methods=["GET"])
def getFollowButton(followeeId=None):
    if (checkSession()):
        if (followeeId != session['id']):
           db = get_db()
           user = getUserFromSql(db.execute('SELECT * FROM USER WHERE user_id=?',[followeeId]))
           if isFollowing(followeeId):
               return render_template("unfollowbutton.html",user=user)
           else:
               return render_template("followbutton.html", user=user)
        else:
            return "null"
    else:
        return "null"

#   returns the userId's of all accounts that are followed by a user currently logged in
def getFolloweeIdsForUser():
    userIds = []
    if (checkSession()):
        db = get_db()
        for uId in db.cursor().execute("SELECT followee_id FROM Follow WHERE follower_id=?", (session['id'])):
            userIds.append(uId[0])
    return userIds




def isFollowing(followeeId):
    db = get_db()
    if (checkSession() == False):
        return False
    for row in db.cursor().execute("SELECT * FROM Follow WHERE follower_id=? AND followee_id=?",(session["id"], followeeId)):
        return True
    return False