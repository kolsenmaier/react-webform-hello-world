import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Instantiate the database
db = SQLAlchemy()

def create_app(script_info=None):
    # Instantiate the app
    app = Flask(__name__)

    # Get config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # Set up extensions
    db.init_app(app)

    # Register blueprints
    from main.api.food import food_blueprint
    app.register_blueprint(food_blueprint)

    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app