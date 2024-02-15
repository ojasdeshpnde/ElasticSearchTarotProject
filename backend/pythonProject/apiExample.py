import io

from elasticsearch import Elasticsearch
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import requests
from PIL import Image
from passlib.context import CryptContext
import secrets
import sqlite3
import User
import jwt
import random

app = Flask(__name__)
CORS(app)

path_to_creds = "../../docker/"
with open(path_to_creds + "cred.txt", encoding="utf8") as file:
    password = file.read()
es = Elasticsearch('https://localhost:9200', ca_certs=path_to_creds + "http_ca.crt", basic_auth=("elastic", "fAhOSOHq_3spLm9ht_tW"))

pwd_context = CryptContext(schemes=["sha256_crypt"])

# x = requests.get("https://api.scryfall.com/cards/56ebc372-aabd-4174-a943-c7bf59e5028d")
#
# b = x.json()['image_uris']['large']
# b = requests.get(b)
# b.raise_for_status()
# # if b.status_code != 204:
# #     print(b.content)



def generate_salt():
    salt_bytes = secrets.token_bytes(8)
    salt_hex = salt_bytes.hex()
    return salt_hex


def hash_password(password, salt):
    tmp = pwd_context.hash(password, salt=salt)
    parts = tmp.split('$')
    extracted_hash = '$'.join(parts[4:])
    return extracted_hash


# @app.route('/fanfic/<fanfic_id>',methods=['GET'])

def createUser(password, fname, lname, email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    check0 = "SELECT EXISTS(SELECT 1 FROM users WHERE email = \"{}\");".format(email)
    checkResult = cursor.execute(check0).fetchone()[0]
    if(checkResult==1):
        return None

    check1 = "SELECT MAX(id) FROM users;"
    tmp = cursor.execute(check1).fetchall()

    generatedSalt = generate_salt()
    saltedPassword = hash_password(password, generatedSalt)

    id = 0
    if (tmp[0][0] != None):
        id = tmp[0][0]

    tmp2 = "INSERT OR IGNORE INTO users VALUES ({},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(int(id)+1,
                                                                                               fname,
                                                                                               lname,
                                                                                               generatedSalt,
                                                                                               saltedPassword,
                                                                                               email)
    cursor.execute(tmp2)

    conn.commit()
    conn.close()

    userObj = User.User(id, fname, lname, email)
    return userObj


def authenticate_user(email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    check1 = "SELECT * FROM users WHERE email = \"{}\";".format(email)
    tmp = cursor.execute(check1).fetchall()

    if(len(tmp) > 0):
        tmp = tmp[0]
        if (tmp[4] == hash_password(password, tmp[3])):
            return User.User(tmp[0], tmp[1], tmp[2], tmp[5])

    conn.close()
    return None

def genSession(payload):
    secret_key = '589b1ea45ae4551b27639cdbdc6fc47d6c4e749ca9d45df423daafc592a623e2'
    obj = {"id":payload.id, "fname":payload.fname , "lname":payload.lname, "email":payload.email}
    encoded_token = jwt.encode(obj, secret_key, algorithm='HS256')

    return encoded_token

    # # Decode (verify) the JWT
    # try:
    #     decoded_payload = jwt.decode(encoded_token, secret_key, algorithms=['HS256'])
    #     print('Decoded Payload:', decoded_payload)
    # except jwt.ExpiredSignatureError:
    #     print('Token has expired.')
    # except jwt.InvalidTokenError:
    #     print('Invalid token.')



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


@app.route('/signup', methods=['POST'])
def sign_up():

    formData = request.get_json()
    user = createUser(formData['password'], formData['fname'], formData['lname'], formData['email'])
    if user != None:
        retObject = jsonify(genSession(user))
        retObject.set_cookie("auth",str(retObject), httponly=True, secure=True)
        return retObject
    else:
        return make_response(jsonify("access denied"), 404)


@app.route('/login', methods=['POST'])
def login():
    formData = request.get_json()
    user = authenticate_user(formData['email'], formData['password'])
    if user != None:
        retObject = jsonify(genSession(user))
        retObject.set_cookie("auth",str(retObject), httponly=True, secure=True)
        return retObject
    else:
        return make_response(jsonify("access denied"), 404)

def searchCardsByName(name, size=10):
    hits = es.search(index="mtgcards", body={"sort": "_score", "size": size, "query": {"bool":
                                                                         {"should": {"match": {"name": {"query": name, "fuzziness": "AUTO"}}},
                                                                          "must": {"match": {"layout": {"query": "normal"}}},
                                                                          }}})['hits']['hits']
    if len(hits) == 0:
        hits = random.choice(es.search(index="mtgcards", body={"query": {"match_all": {}}})['hits']['hits'])
        # print(hits)
    else:
        weights = [0]*len(hits)
        for i, j in enumerate(hits):
            weights[i] = j["_score"]
        # just weighting by the score
        hits = random.choices(hits, weights=weights, k = 1)[0]
    hits=hits['_source']
    if 'image_uris' in hits:
        return hits['image_uris']['large']
    elif 'card_faces' in hits:
        print(hits['card_faces'])
        return random.choice(hits['card_faces'])['image_uris']['large']
    else:
        return searchCardsByName("")
@app.route('/getcard',methods=['POST'])
def getcard():
    query = request.get_json()
    b = searchCardsByName(query)
    b = requests.get(b)
    b.raise_for_status()
    response = make_response(b.content)
    image = Image.open(io.BytesIO(b.content))
    width, height = image.size
    left = 80 * width / 672
    right = 592 * width / 672
    top = 92 * height / 936
    bottom = 500 * height / 936
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
    app.run(host="0.0.0.0", port=5002,debug=False)
