from flask import Blueprint, render_template, request, redirect,url_for

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("base.html", title = "Finddit")

@views.route('/signuplogin.html')
def signuplogin():
    return render_template("signuplogin.html")

@views.route('/events.html')
def events():
    return render_template("events.html")

@views.route('/results.html')
def results():
    return render_template("results.html")
