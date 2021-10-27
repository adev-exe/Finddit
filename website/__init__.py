import os

from flask import Flask
from flask.helpers import url_for

def create_app():
    app = Flask(__name__,
        static_url_path='',
        static_folder='static'
    )
    
    app.config.from_mapping(
        SECRET_KEY='huh',
        DATABASE=os.path.join(app.instance_path, 'website.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from . import findditDB
    findditDB.init_app(app)

    return app
