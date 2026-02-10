from flask import Flask
from datetime import timedelta
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder="../static", template_folder="templates")
    app.secret_key = os.environ.get("SECRET_KEY")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SESSION_PERMANENT"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)

    #Initialize limiter
    limiter.init_app(app)


    from app.routes import register_blueprint
    register_blueprint(app)

    return app


