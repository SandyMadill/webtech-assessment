from flask import session, render_template

from database import get_db


class User:
    def __init__(self, userId,  username, displayName, role):
        self.userId = userId
        self.username = username
        self.displayName = displayName
        self.role = role

def getUserFromSql(sql):
    for u in sql:
        print(u)
        user = User(u[0], u[1], u[3], u[4])
        print(str(u))
        return user
    return None

def getUser(id):
    db = get_db()
    return getUserFromSql(db.cursor().execute("SELECT * FROM User WHERE user_id = ?", [id]))

def checkSession():
    try:
        if(session['id']):
            return True
        else:
            return False
    except KeyError:
        return False