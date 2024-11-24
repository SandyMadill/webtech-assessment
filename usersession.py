from flask import session

class UserSession:
    def __init__(self, user_id, role):
        self.user_id = int(user_id)
        self.role = role


def getSession():
    if checkSession():
        return UserSession(session['id'], session['role'])
    else:
        return None

def checkSession():
    try:
        if(session['id']):
            return True
        else:
            return False
    except KeyError:
        return False