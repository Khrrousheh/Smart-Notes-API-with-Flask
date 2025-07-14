from flask import Flask
from flasgger import Swagger
from app.models import db
from app.routes.notes import notes_bp
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Swagger(app)
    app.register_blueprint(notes_bp)

    with app.app_context():
        db.create_all()

    return app
