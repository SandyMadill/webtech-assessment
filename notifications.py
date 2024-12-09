import datetime

import flask
from flask import Blueprint, render_template, session

from database import get_db
from user import getUser
from usersession import checkSession, getSession
notificationApi = Blueprint('notification-api', __name__, template_folder='templates')

class Notification:
    def __init__(self, userId, interactingUserId, postId, action, seen, dateAndTime):
        self.userId = userId
        self.interactingUserId = interactingUserId
        self.postId = postId
        self.action = action
        self.seen = seen
        self.dateAndTime = dateAndTime

#renders the notification page
@notificationApi.route('/notifications/', methods=['GET'])
def renderNotificationPage():
    # check if the user is logged in
    if checkSession():
        # get this users notifications
        notifications = getNotifications()
        return render_template("index.html", page="notifications", newNotifications=notifications[0], oldNotifications = notifications[1], userSession = getSession())


# updates all unseen notifications belonging to the user to seen
@notificationApi.route('/notifications/seen/', methods=['PUT'])
def seenNotification():
    if checkSession():
        db = get_db()
        db.cursor().execute("UPDATE Notification SET seen=true WHERE user_id=?", ([session['id']]))
        db.commit()
        return "success"

# returns all of the logged in users notifications as a tuple containing two arrays:
# one containing the new notification the other containing the old notifications
# the notifications are stored as rendered html notification templates
def getNotifications():
    db = get_db()
    newNotifications = []
    oldNotifications = []
    for n in db.cursor().execute("SELECT * FROM Notification WHERE user_id=? ORDER BY date_and_time DESC", [session['id']]):
        notif = Notification(n[0],n[1],n[2],n[3],bool(n[4]),n[5])
        user = getUser(notif.interactingUserId)

        # if the action was a follow then the notification wont have a post
        # in all other cases the notification will have a post so get the text from that post
        if notif.action != "follow":
            for pt in db.cursor().execute("SELECT post_text FROM Post WHERE post_id=?", [str(notif.postId)]):
                postText = pt[0]
        else:
            postText = None

        print(postText)
        #rendered the notification
        temp = flask.render_template("notification.html", notification=notif, user=user, postText=postText)

        if notif.seen==False:
            newNotifications.append(temp)
        else:
            oldNotifications.append(temp)
    return [newNotifications, oldNotifications]

# adds a notification to the Notification table
def makeNotification(userId, interactingUserId, postId, action):
    if (userId != interactingUserId):
        db = get_db()

        db.cursor().execute("INSERT INTO Notification(user_id, interacting_user_id, post_id, action, seen, date_and_time) VALUES(?, ?, ?, ?, ?, ?)", (userId, interactingUserId, postId, action, False, datetime.datetime.now()))
        db.commit()

def deleteNotification(userId, interactingUserId, postId, action):
    if (userId != interactingUserId):
        db = get_db()
        if postId == None:
            db.cursor().execute("DELETE FROM Notification WHERE user_id=? AND interacting_user_id=? AND action=?", (userId, interactingUserId, action))
        else:
            db.cursor().execute("DELETE FROM Notification WHERE user_id=? AND interacting_user_id=? AND post_id=? AND action=?", (userId, interactingUserId, postId, action))
        db.commit()