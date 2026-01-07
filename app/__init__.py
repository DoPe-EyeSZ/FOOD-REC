from flask import Flask
from datetime import timedelta
from dotenv import load_dotenv
import os


def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder="../static", template_folder="templates")
    app.secret_key = os.environ.get("SECRET_KEY")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SESSION_PERMANENT"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)


    from app.routes import register_blueprint
    register_blueprint(app)

    return app


