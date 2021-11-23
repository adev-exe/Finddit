import os
from flask import Blueprint, render_template, request, redirect,url_for
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

@views.route('/signuplogin.html')
def signuplogin():
    return render_template("signuplogin.html")

@views.route('/events.html')
def events():
    description = 'Description'
    return render_template("events.html",  description = 'Description')

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

@views.route('/reviewResult.html')
def review_result():
    return render_template("reviewResult.html", title = "Finddit")

@views.route("/location/<id>", methods=['GET'])
def location(id):
    place=get_details(id, secrets["api_key"])
    place=process_result(place)
    return render_template("location.html", location=place)
