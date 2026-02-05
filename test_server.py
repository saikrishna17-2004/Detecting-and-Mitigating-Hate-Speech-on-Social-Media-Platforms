"""
Simple test to see if Flask works
"""
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'message': 'Server is working!'})

@app.route('/test')
def test():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    print("Starting test server on port 5001...")
    app.run(debug=True, port=5001)
