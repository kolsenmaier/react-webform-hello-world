import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Instantiate the database
db = SQLAlchemy()

def create_app(script_info=None):
    # Instantiate the app
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Get config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # Set up extensions
    db.init_app(app)

    # Register blueprints
    from main.api.foodcategories import food_categories_blueprint
    app.register_blueprint(food_categories_blueprint)
    from main.api.foodtypes import food_types_blueprint
    app.register_blueprint(food_types_blueprint)
    from main.api.submissions import submissions_blueprint
    app.register_blueprint(submissions_blueprint)

    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app