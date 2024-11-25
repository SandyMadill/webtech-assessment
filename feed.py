import datetime

from flask import Blueprint, render_template, session, request

from config import config
from database import get_db
from follow import getFolloweeIdsForUser
from postlist import getPostListWithWhereClause
from user import checkSession, getUserFromSql

feedApi = Blueprint('feed-api', __name__, template_folder='templates')

@feedApi.route('/feed', methods=['GET'])
def getFeed():
    followees = getFolloweeIdsForUser()
    where = ""
    for i in range(len(followees)):
        where += "user_id=" + str(followees[i])
        if(i+1 < len(followees)):
            where += " AND "
    return(getPostListWithWhereClause(str(datetime.datetime.now()), "desc", where))
