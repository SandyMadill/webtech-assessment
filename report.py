import json
from xmlrpc.client import DateTime

from flask import Blueprint, request, render_template, session
import datetime
from database import get_db
from post import getPost, getPostById
from user import getUser
from usersession import checkSession, getSession

reportApi = Blueprint('report-api', __name__, template_folder='templates')

#   defines the properties of a report
class Report:
    def __init__(self, reportId, explanation, postId, reportedId, reporterId, reportSorted, date_and_time):
        self.reportId = reportId
        self.explanation = explanation
        self.postId = postId
        self.reportedId = reportedId
        self.reporterId = reporterId
        self.reportSorted = reportSorted
        self.date_and_time = date_and_time



@reportApi.route('/report/<userId>/<postId>', methods=['GET', 'POST'])
def reportUser(userId=None,postId=None):
    if checkSession():
        if request.method == "GET":
            return render_template("index.html" , page="report", reportMade=False, userSession = getSession())
        elif request.method == "POST":
            reporterId = session["id"]
            explanation = request.form.get("explanation")
            db = get_db()
            db.cursor().execute("INSERT INTO Report(explanation, post_id, reported_id, reporter_id, sorted, date_and_time) VALUES (?, ?, ?, ?, false, ?)", (explanation, postId, userId, reporterId, datetime.datetime.now()))
            db.commit()
            return render_template("index.html", page="report", reportMade=True, userSession = getSession())

@reportApi.route('/report/<userId>/', methods=['GET', 'POST'])
def reportUserWithPost(userId=None):
    return reportUser(userId, None)

#   gets the oldest report that has not been sorted
@reportApi.route('/report/next/', methods=['GET', 'POST'])
def getNextReport():
        if checkSession():
            userSession = getSession()
            if userSession.role == "mod":
                db = get_db()
                for r in db.cursor().execute("SELECT * FROM Report WHERE sorted = FALSE ORDER BY date_and_time ASC LIMIT 1"):
                    report = Report(r[0], r[1], r[2], r[3], r[4], bool(r[5]), r[6])
                    return report

                return None

#   will render the view reports page for admins only
@reportApi.route('/report/view/', methods=['GET', 'POST'])
def reportView():
    if checkSession():
        userSession = getSession()
        if userSession.role == "mod":
            report = getNextReport()
            reporter = None
            reported = None
            post = None
            if report != None:
                if report.postId !=None:
                    post = getPostById(report.postId)
                reporter = getUser(report.reporterId)
                reported = getUser(report.reportedId)
            return render_template("index.html", page="view-reports", report=report, reporter=reporter, user=reported, post=post, rpUser = None, userSession = getSession())

@reportApi.route('/ban/<reportId>/<userId>', methods=['PUT'])
def ban(userId,reportId):
    if checkSession():
        userSession = getSession()
        if userSession.role == "mod":
            permanant = request.form.get("permanent")
            unbanDate = request.form.get("unbanDate")
            db = get_db()
            if permanant == "true":
                db.cursor().execute("UPDATE User SET banned = TRUE WHERE user_id = ?", (userId,))
                db.commit()
            else:
                db.cursor().execute("UPDATE User SET banned = TRUE, unban_date = ? WHERE user_id = ?", (unbanDate,userId))
                db.commit()
            db.cursor().execute("UPDATE Report SET sorted = TRUE WHERE report_id = ?", (reportId,))
            db.commit()
            return "User-Banned"

@reportApi.route('/report/ignore/<reportId>/', methods=['PUT'])
def ignore(reportId=None):
    if checkSession():
        userSession = getSession()
        if userSession.role == "mod":
            db = get_db()
            db.cursor().execute("UPDATE Report SET sorted = TRUE WHERE report_id = ?", (reportId,))
            db.commit()
            return "Report-Ignored"
