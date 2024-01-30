import io

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import requests
from PIL import Image

app = Flask(__name__)
CORS(app)


x = requests.get("https://api.scryfall.com/cards/56ebc372-aabd-4174-a943-c7bf59e5028d")

b = x.json()['image_uris']['large']
print(b)
b = requests.get(b)
b.raise_for_status()
if b.status_code != 204:
    print(b.content)

@app.route('/')
def hello_world():
    return jsonify('Hello, World!')

@app.route('/testimage')
def blah():
    response = make_response(b.content)
    image = Image.open(io.BytesIO(b.content))
    width, height = image.size
    left = 80*width/672
    right = 592*width/672
    top = 92*height/936
    bottom = 500*height/936
    img_byte_arr = io.BytesIO()
    image.crop((left, top, right, bottom)).save(img_byte_arr, format='jpeg')
    img_byte_arr = img_byte_arr.getvalue()
    image.close()
    response = make_response(img_byte_arr)
    # this might be helpful
    response.headers.set('Content-Type', 'image/jpeg')
    # below will start a download
    # response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % 'test')
    return response
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001,debug=False)
