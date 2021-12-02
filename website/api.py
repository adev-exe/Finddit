from flask import Blueprint, render_template, request, redirect,url_for, jsonify, Response
from munch import munchify
import yaml
import requests, json
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
    
@api.route("/login", methods=['POST'])
def do_login():
    db = get_db()
    cur = db.cursor()
    f = munchify(request.form)
    cur.execute("INSERT INTO user (username, password, first_name, last_name, email) \
    VALUES ({}, {}, {}, {}, {})".format(f.username, f.password, f.first_name, f.last_name, f.email))
    db.commit()
    print ("{} registered successfully".format(f.username))
    return "hi"
