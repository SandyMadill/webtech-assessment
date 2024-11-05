from flask import render_template, request, session
from database import get_db
import datetime

def initCreatePost():
    try:
        if (session['id'] and session['role']):
            db = get_db()
            if (request.method == 'POST'):
                userId = session['id']
                text = request.form['text']
                db.cursor().execute("INSERT INTO Post(user_id, post_text, has_images, date_and_time) VALUES(?,?,false,?)", (userId, text, datetime.datetime.now()));
                db.commit()

        else:
            return "AAAAAAAAA"

        return render_template('create-post.html')
    except KeyError:
        return "rejwfkjrehfkjewhkfjhewfrA"

