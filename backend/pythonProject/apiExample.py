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
CORS(app, supports_credentials=True)


path_to_creds = "../../docker/"
with open(path_to_creds + "cred.txt", encoding="utf8") as file:
    password = file.read()
es = Elasticsearch('https://localhost:9200', ca_certs=path_to_creds + "http_ca.crt", basic_auth=("elastic", password))

pwd_context = CryptContext(schemes=["sha256_crypt"])


# if b.status_code != 204:
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

    tmp2 = "INSERT OR IGNORE INTO users VALUES ({},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\", 0, 0, 0, 0, 0, 0, 0)".format(int(id)+1,
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

def storeReading(imageLink, text1, text2, text3, text4, text5):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    check1 = "SELECT MAX(id) FROM cardReadings;"
    tmp = cursor.execute(check1).fetchall()

    id = 0
    if (tmp[0][0] != None):
        id = tmp[0][0]

    tmp2 = "INSERT OR IGNORE INTO cardReadings VALUES ({},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(int(id)+1,
                                                                                               imageLink,
                                                                                               text1,
                                                                                               text2,
                                                                                               text3,
                                                                                               text4,
                                                                                               text5)
        
    cursor.execute(tmp2)

    conn.commit()
    conn.close()

    userID = CallToJWTToGetActiveUser()
    storeCardToUser(int(id) + 1, userID) 

#shifts current cards 1-7 to next position updates card1 with newestReading
def storeCardToUser(cardID, userID):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    #get current cards
    cards = list(cursor.execute("SELECT card1, card2, card3, card4, card5, card6, card7 FROM users WHERE id = ?", (userID,)).fetchone())
    
    #shift cards
    for i in range(len(cards) - 2, -1, -1):
        if cards[i] != 0:
            cards[i+1] = cards[i]
    
    #assign newest Card
    cards[0] = cardID

    #update database
    updateData = """
        UPDATE users
        SET card1 = ?, card2 = ?, card3 = ?, card4 = ?, card5 = ?, card6 = ?, card7 = ?
        WHERE id = ?
        """
    cursor.execute(updateData, (*cards, userID))

    conn.commit()
    conn.close()


#Returns (CardID, imageLink, text1-5) tuple
def getRecentCards(NumOfCard, userID):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    #get cards
    cards = list(cursor.execute("SELECT card1, card2, card3, card4, card5, card6, card7 FROM users WHERE id = ?", (userID,)).fetchone())

    #get card's unique id 
    cardID = cards[NumOfCard - 1]
    cardInfo = cursor.execute("SELECT * FROM cardReadings where id = ?", (cardID,)).fetchone()
    conn.close()

    #return card
    return cardInfo

def CallToJWTToGetActiveUser():
    return 1

def decodeToken(jwToken):
    secret_key = '589b1ea45ae4551b27639cdbdc6fc47d6c4e749ca9d45df423daafc592a623e2'
    try:
        decoded_payload = jwt.decode(jwToken, secret_key, algorithms='HS256')
        return decoded_payload['id']
    except jwt.ExpiredSignatureError:
        print('Token has expired.')
    except jwt.InvalidTokenError:
        print('Invalid token.')
    return -1

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






@app.route('/')
def hello_world():
    return jsonify('Hello, World!')

@app.route('/testimage')
def blah():
    print(decodeToken(request.cookies.get('auth')))

    x = requests.get("https://api.scryfall.com/cards/56ebc372-aabd-4174-a943-c7bf59e5028d")
    b = x.json()['image_uris']['large']
    b = requests.get(b)
    b.raise_for_status()
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

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/signup', methods=['POST'])
def sign_up():

    formData = request.get_json()
    user = createUser(formData['password'], formData['fname'], formData['lname'], formData['email'])
    if user != None:
        retObject = genSession(user)
        token = retObject
        retObject = jsonify(retObject)
        retObject.set_cookie("auth",str(token),httponly=True, samesite="None", secure=True)
        add_cors_headers(retObject)
        return retObject
    else:
        return make_response(jsonify("access denied"), 404)


@app.route('/login', methods=['POST'])
def login():
    formData = request.get_json()
    user = authenticate_user(formData['email'], formData['password'])
    if user != None:
        retObject = genSession(user)
        token = retObject
        retObject = jsonify(retObject)
        retObject.set_cookie("auth",str(token),httponly=True, samesite="None", secure=True)
        add_cors_headers(retObject)
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
