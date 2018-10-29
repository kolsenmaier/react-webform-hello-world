from flask import Flask, jsonify

# Instantiate the app
app = Flask(__name__)

@app.route('/food', methods=['GET'])
def get_food():
    return jsonify({
        'status': 'success',
        'message': 'bread'
    })