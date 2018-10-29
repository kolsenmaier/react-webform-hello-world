import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Instantiate the app
app = Flask(__name__)

# Get config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# Instantiate the database
db = SQLAlchemy(app)

# Datamodel
class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.String(128), nullable=False)
    isvisible = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, category, type, amount):
        self.category = category
        self.type = type
        self.amount = amount

# GET visible food table contents (TODO return from DB)
@app.route('/food', methods=['GET'])
def get_food():
    return jsonify({
        'status': 'success',
        'message': 'bread'
    })