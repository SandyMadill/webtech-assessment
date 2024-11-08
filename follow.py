from flask import Blueprint, render_template, session, request
from database import get_db

simple_page = Blueprint('simple_page', __name__, template_folder='templates')
@simple_page.route('/follow/<followeeId>')
def init_follow(followeeId=None):
    db=get_db()

    sql = db.execute("SELECT EXISTS(SELECT 1 FROM Follow WHERE follower_id=? AND followee_id=?) AS follow_exists",[2,1])
    print(sql[0])
    for row in sql:
        print (str(row))
        return str(row)
    return "AAAAAAAAAAAAAAA"
