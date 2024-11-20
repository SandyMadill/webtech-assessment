from flask import session
class User:
    def __init__(self, userId,  username, displayName, role):
        self.userId = userId
        self.username = username
        self.displayName = displayName
        self.role = role

def checkSession():
    try:
        if(session['id']):
            return True
        else:
            return False
    except KeyError:
        return False