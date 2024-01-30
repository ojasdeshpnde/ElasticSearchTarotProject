from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


x = requests.get("https://api.scryfall.com/cards/56ebc372-aabd-4174-a943-c7bf59e5028d")

print(x.json())


@app.route('/')
def hello_world():
    return jsonify('Hello, World!')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001,debug=False)
