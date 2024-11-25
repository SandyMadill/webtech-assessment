import datetime
from Xlib.ext.randr import PROPERTY_CLONE_LIST
from click import DateTime
from flask import Flask, Blueprint, render_template, logging

from config import config
from database import get_db
from post import getPostFromSql, getPost

postListApi = Blueprint('post-list-api', __name__, template_folder='templates')


@postListApi.route('/post-list/<afterDate>/<ord>', methods=['GET'])
def getPostList(afterDate = None, ord = None):
    if (ord == "desc"):
        db = get_db()
        posts = []

        lastDate=None
        for p in db.cursor().execute("SELECT post_id, date_and_time FROM Post WHERE date_and_time < ? ORDER BY date_and_time DESC LIMIT 10", [afterDate]):
            posts.append(getPost(p[0]))
            lastDate=p[1]
        return [posts, lastDate]
    else:
        db = get_db()
        posts = []
        LastDate = None
        for p in db.cursor().execute("SELECT post_id, date_and_time FROM Post WHERE date_and_time > ? ORDER BY date_and_time ASC LIMIT 10", [afterDate]):
            posts.append(getPost(p[0]))
            lastDate = p[1]
        return [posts]

@postListApi.route('/post-list/<afterDate>/<ord>/<where>', methods=['GET'])
def getPostListWithWhereClause(afterDate = None, ord = None, where = None):
    if (ord == "desc"):
        db = get_db()
        posts = []
        print(where + " AND date_and_time < " + afterDate)
        lastDate=None
        log_and_execute(db.cursor(),"SELECT post_id, date_and_time FROM Post WHERE ? ORDER BY date_and_time DESC LIMIT 10", ("date_and_time < " + afterDate))
        sql =  db.cursor().execute("SELECT post_id, date_and_time FROM Post WHERE ? ORDER BY date_and_time DESC LIMIT 10", ["date_and_time < " + afterDate])
            #print("aaaaaaaa")
            #posts.append(getPost(p[0]))
            #lastDate=p[1]


        return [posts, lastDate]
    else:
        db = get_db()
        posts = []
        LastDate = None
        for p in db.cursor().execute("SELECT post_id, date_and_time FROM Post WHERE date_and_time > ? ORDER BY date_and_time ASC LIMIT 10", [afterDate]):
            posts.append(getPost(p[0]))
            lastDate = p[1]
        return [posts]

def log_and_execute(cursor, sql, *args):
    s = sql
    if len(args) > 0:
        # generates SELECT quote(?), quote(?), ...
        cursor.execute("SELECT " + ", ".join(["quote(?)" for i in args]), args)
        quoted_values = cursor.fetchone()
        for quoted_value in quoted_values:
            s = s.replace('?', quoted_value, 1)
            #s = re.sub(r'(values \(|, | = )\?', r'\g<1>' + quoted_value, s, 1)
    print("SQL command: " + s)
    cursor.execute(sql, args)