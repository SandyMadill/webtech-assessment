from flask import Blueprint, render_template, session, request
from database import get_db
from user import checkSession

follow = Blueprint('simple_page', __name__, template_folder='templates')
@follow.route('/follow/<followeeId>')
def init_follow(followeeId=None):
    if checkSession():
        return render_template("follow.html", userId=followeeId)
    else:
        return None
@follow.route('/follow/follow-user/<followeeId>', methods=["POST"])
def followUser(followeeId=None):
    if (checkSession() and isFollowing(followeeId) == False):
        db=get_db()
        db.cursor().execute("INSERT INTO Follow(follower_id, followee_id) VALUES(?,?)", (session['id'], followeeId))
        db.commit()
        return getFollowButton(followeeId)
    else:
        return None

@follow.route('/follow/unfollow-user/<followeeId>', methods=["POST"])
def unfollowUser(followeeId=None):
    if (checkSession() and isFollowing(followeeId)):
        db=get_db()
        db.cursor().execute("DELETE FROM Follow WHERE follower_id=? AND followee_id=?", (session['id'], followeeId))
        db.commit()
        return getFollowButton(followeeId)
    else:
        return None
@follow.route('/follow/button/<followeeId>', methods=["GET"])
def getFollowButton(followeeId=None):
    if (checkSession()):
           db = get_db()
           if isFollowing(followeeId):
               return render_template("unfollowbutton.html",userId=followeeId)
           else:
               return render_template("followbutton.html", userId=followeeId)

    else:
        return None

def isFollowing(followeeId):
    if (checkSession()):
        db = get_db()
        for row in db.cursor().execute("SELECT * FROM Follow WHERE follower_id=? AND followee_id=?",(session["id"], followeeId)):
            return True
        return False
    else:
        return False
