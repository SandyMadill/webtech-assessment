from flask import Blueprint, render_template, session, request
from database import get_db

simple_page = Blueprint('simple_page', __name__, template_folder='templates')
@simple_page.route('/follow/<followeeId>')
def init_follow(followeeId=None):
    db=get_db()

    db.cursor().execute("SELECT EXISTS(SELECT 1 FROM Follow WHERE follower_id=? AND followee_id=?) AS follow_exists",(session["id"],followeeId))
    sql = db.cursor().fetchall()
    if len(sql) == 0:
        return render_template("follow.html", userId=followeeId, following="true")
    else:
        return "FOUND"

@simple_page.route('/follow/<followeeId>', methods=["POST"])
def followUser(followeeId=None):
    db=get_db()
    print("df;gkjdflkgjdflkgjdfljkghdfjlkghdlfjkgh")
    db.cursor().execute("SELECT EXISTS(SELECT 1 FROM Follow WHERE follower_id=? AND followee_id=?) AS follow_exists",(session["id"],followeeId))
    sql = db.cursor().fetchall()
    if len(sql) == 0:
        return "AAAAAAAAAAAAAAAAAAA"
    else:
        return "FOUND"

