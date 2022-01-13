from flask import Flask
import toml


def create_app():
    app = Flask(__name__)
    app.config.from_file('../config.toml', toml.load)

    # register blueprints
    @app.get('/')
    def home():
        return 'Hello from FLASK'

    return app
