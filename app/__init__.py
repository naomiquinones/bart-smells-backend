from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_cors import CORS
from colorama import init, Fore, Back, Style
# below init is for colorama
# use autoreset=True to reset colorama
init(autoreset=True)

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DB_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DB_URI_TEST")

    # Import models here for Alembic setup
    from app.models.report import Report
    from app.models.rider import Rider

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here

    from .routes import root_bp
    from .routes import reports_bp
    from .routes import riders_bp
    from .routes import login_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(root_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(riders_bp)

    print("\n" + '\033[45m' + Fore.BLACK + "*-*-*-       Creating app" + "      *-*-*-        Yay!")

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    # CORS(app, origins=["http://localhost:5173", "http://localhost:5173"])
    return app