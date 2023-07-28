"""Initialize Flask app."""
from os import path

from flask import Flask

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile(path.abspath(path.dirname(path.dirname(__file__))) + "/flask_config.py")

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        return app
