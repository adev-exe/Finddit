import requests, json
from munch import munchify

# url variable store url
search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
details_url = "https://maps.googleapis.com/maps/api/place/details/json?"

def get_details(id, key):
    r = requests.get(details_url + "place_id=" + id + '&key=' + key)
    x = r.json()
    return x

def search(query, key):
    r = requests.get(search_url + 'query=' + query + '&key=' + key)
    x = r.json()
    x = x['results']
    x = munchify(x)
    return x

def process_result(r):
    return {
    "address" : r.formatted_address,
    "icon" : r.icon,
    "name" : r.name,
    "photo" : r.photos[0].photo_reference if "photos" in r else None,
    "location" : r.geometry.location
    }

def photo_url(reference, key, width=400):
  return "https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photo_reference={}&key={}".format(
    width,
    reference,
    key
  )
