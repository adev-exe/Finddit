from flask import Flask
from flask.helpers import url_for

def create_app():
    app = Flask(__name__,
        static_url_path='',
        static_folder='static'
    )
    
    app.config['SECRET_KEY'] = 'huh'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app