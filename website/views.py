from flask import Blueprint, render_template, request, redirect,url_for

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/signuplogin.html')
def signuplogin():
    return render_template("signuplogin.html")


@views.route('/login', methods=['GET', 'POST'])
def index_func():
    if request.method == 'POST':
       
        return redirect(url_for('index'))
    return render_template('login.html')