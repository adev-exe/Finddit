import os
import functools
from flask import (
    Blueprint, render_template, request, redirect,url_for, session, flash, g
)
from .reviews import add_review, get_reviews
from werkzeug.security import check_password_hash, generate_password_hash
from website.findditDB import get_db
from werkzeug.utils import append_slash_redirect
from .api import secrets
from .api_utils import get_details, process_result

views = Blueprint('views',__name__)

# imagesFolder = os.path.join('static', 'images')
# app.config['UPLOAD_FOLDER'] = imagesFolder

@views.route('/')
@views.route('/base.html')
def home():
    # logo = os.path.join(app.config['UPLOAD_FOLDER'], 'Finddit.gif')
    return render_template("base.html", title = "Finddit")

@views.route('/signuplogin.html', methods=['GET'])
def signuplogin():
    return render_template("views/signuplogin.html")

@views.before_app_request
def load_logged_in_user():
    user_first_name = session.get('user_first_name')
    user_email = session.get('email')

    if user_email is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE email = ?', (user_email,)
        ).fetchone()

@views.route('/events.html')
def events():
    description = 'Description'
    #get all events from the database and put them on the page
    db = get_db()
    posts = db.execute(
        'SELECT e_id, event_name, event_date, event_time, event_desc'
        ' FROM event'
    ).fetchall()
    return render_template("events.html",  description = 'Description', posts=posts)

#route for creating an event page
@views.route('/create.html', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        event = request.form['eventN']
        e_date = request.form['e_date']
        e_time = request.form['e_time']
        e_desc = request.form['e_desc']
        error = None

        if not event:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO event (event_name, event_date, event_time, event_desc)'
                ' VALUES (?, ?, ?, ?)',
                (event, e_date, e_time, e_desc)
            )
            db.commit()
            return render_template('events.html')
    return render_template('create.html')

@views.route('/login', methods=['GET', 'POST'])
def index_func():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html')

@views.route('/result.html')
def results_details():
    return render_template("result.html")

@views.route('/review.html')
def review():
    return render_template("review.html", title = "Finddit")

@views.route('/location/<id>/reviewResult.html', methods=['GET', 'POST'])
def review_result(id):
    if request.method == 'POST':
        rate = request.form['rate']
        content = request.form['content']
        print(rate, content)
        add_review(id, session["email"], session["user_first_name"], rate, content)
        return redirect(url_for('views.location', id = id))
    return render_template("reviewResult.html", title = "Finddit", id = id)

@views.route("/location/<id>", methods=['GET'])
def location(id):
    place=get_details(id, secrets["api_key"])
    place=process_result(place)
    reviews = get_reviews(id)
    print(reviews)
    return render_template("location.html", location=place, reviews = reviews)
