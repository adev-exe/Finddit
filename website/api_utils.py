import requests, json
from munch import munchify

# url variable store url
search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
details_url = "https://maps.googleapis.com/maps/api/place/details/json?"
nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

def nearby_search(lat, lon, radius, place_type, key):
    r = requests.get(search_url + "location={}%2C{}&radius={}&type={}&query={}&key={}".format(
    lat, lon, radius, place_type, place_type.replace('_',' '), key))
    x = r.json()
    x = x['results']
    x = munchify(x)
    return x

def get_details(id, key):
    r = requests.get(details_url + "place_id=" + id + '&key=' + key)
    x = r.json()
    x = x['result']
    x = munchify(x)
    return x

def search(query, key):
    r = requests.get(search_url + 'query=' + query + '&key=' + key)
    x = r.json()
    x = x['results']
    x = munchify(x)
    return x

def get_opening_hours(hours):
    if "opening_hours" not in hours : return None
    hours = hours.opening_hours
    if "weekday_text" not in hours : return None
    return hours.weekday_text

def process_result(r):
    return {
    "address" : r.formatted_address if "formatted_address" in r else "",
    "icon" : r.icon,
    "name" : r.name,
    "photo" : r.photos[0].photo_reference if "photos" in r else None,
    "location" : r.geometry.location,
    "id" : r.place_id,
    "phone" : r.formatted_phone_number if "formatted_phone_number" in r else None,
    "opening_hours" : get_opening_hours(r)
    }

def photo_url(reference, key, width=400):
  return "https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photo_reference={}&key={}".format(
    width,
    reference,
    key
  )

# https://developers.google.com/maps/documentation/places/web-service/details#PlaceReview
# def place_review(author_name, rating, text, key):
#     r = requests.get(nearby_url + "author_name=" + "{}" + "rating=" + "[]" + "text=" + "{}" + '&key=' + key)
#     x = r.json()
#     x = x['result']
#     x = munchify(x)
#     return x
