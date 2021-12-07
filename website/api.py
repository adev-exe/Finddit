from flask import Blueprint, render_template, request, redirect,url_for, jsonify, Response, session, flash
from munch import munchify
import yaml
import requests, json
from werkzeug.security import check_password_hash, generate_password_hash
from .api_utils import get_details, search, process_result, photo_url, nearby_search
from .findditDB import get_db

ECU_LAT = 35.6066043
ECU_LON = -77.3669808

with open("secret.yaml", "r") as file:
    secrets = yaml.safe_load(file)

api = Blueprint('api',__name__)

@api.route("/search", methods=['POST'])
def do_search():
    query = request.form['query']
    # print(request.data)
    results = search(query, secrets["api_key"])
    results = [process_result(r) for r in results]
    #results = jsonify(results)
    # return jsonify("https://maps.googleapis.com/maps/api/place/photo?photoreference=" + results[0]["photos"][0]["photo_reference"])
    return render_template('results_details.html', results=results)
    # return("hello")
    # return render_template('index.html')

@api.route("/photo/<reference>", methods=['GET'])
def get_photo(reference):
    photo = requests.get(photo_url(reference, secrets["api_key"]))
    return Response(photo.content, mimetype='image/png')

@api.route("/nearby-search/<place_type>", methods=['GET'])
def do_nearby_search(place_type):
    results = nearby_search(ECU_LAT, ECU_LON, 10000, place_type, secrets["api_key"])
    results = [process_result(r) for r in results]
    return render_template('results_details.html', results=results)

# @api.route("/login", methods=['POST'])
# def do_login():
#     db = get_db()
#     cur = db.cursor()
#     f = munchify(request.form)
#     cur.execute("INSERT INTO user (username, password, first_name, last_name, email) \
#     VALUES ({}, {}, {}, {}, {})".format(f.username, f.password, f.first_name, f.last_name, f.email))
#     db.commit()
#     print ("{} registered successfully".format(f.username))
#     return "hi"

#getting the login information entered into the login side of page
#and checking if the email and password are correct
@api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email2 = request.form['email']
        password2 = request.form['password']
        findditDB = get_db()
        error = None
        user = findditDB.execute( 'SELECT * FROM user WHERE email = ?', (email2,)).fetchone()
        if user is None:
            error = 'Email is wrong.'
        elif not check_password_hash(user['password'], password2):
            error = 'Password is wrong.'

        if error is None:
            session.clear()
            #session['user_first_name'] = user['first_name']
            session['email'] = user['email']
            return redirect(url_for('views.home'))

        flash(error)
    return redirect(url_for('views.signuplogin'))

@api.route('/signup', methods=['POST'])
def signup():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    findditDB = get_db()
    error = None
    if not firstname:
        error = 'First name required.'
    elif not lastname:
        error = 'Last name required.'
    elif not email:
        error = 'Email required.'
    elif not password:
        error = 'password name required.'
    if error is None:
        try:
            findditDB.execute(
                "INSERT INTO user (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
                (firstname, lastname, email, generate_password_hash(password)),
            )
            findditDB.commit()
        except findditDB.IntegrityError:
            error = f"Email {email} is already signed up"
        else:
            return redirect(url_for("views.signuplogin"))

    flash(error)
    return redirect(url_for('views.signuplogin'))
