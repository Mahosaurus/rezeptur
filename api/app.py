"""Application entry point."""
from os import path

from application import init_app

app = init_app()
app.config.from_pyfile(path.abspath(path.dirname(__file__)) + "/flask_config.py")
app.secret_key = "123"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
