import pickle
from collections import defaultdict

# sorry, Jahmad, feel free to put this in database :)
try:
    with open("reviews.pickle", "rb") as f:
        reviews = pickle.load(f)
except:
    reviews = defaultdict(list)

def add_review(place_id, email, name, rating, content):
  reviews[place_id].append({
    "email": email,
    "name": name,
    "rating": rating,
    "content": content
  })

  with open("reviews.pickle", "wb") as f:
      pickle.dump(reviews, f)

def get_reviews(place_id):
    return reviews[place_id]
