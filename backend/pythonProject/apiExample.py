import io
import re
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
from transformers import pipeline
import pandas as pd

app = Flask(__name__)
CORS(app, supports_credentials=True)

bad_words = pd.read_excel("../prepositions.xlsx")["preposition"].tolist()
path_to_creds = "../../docker/"
with open(path_to_creds + "cred.txt", encoding="utf8") as file:
    password = file.read()
es = Elasticsearch('https://localhost:9200', ca_certs=path_to_creds + "http_ca.crt", basic_auth=("elastic", password))

pwd_context = CryptContext(schemes=["sha256_crypt"])

df = pd.read_excel(path_to_creds + 'datafiles/PromptCategories.xlsx') # can also index sheet by name or fetch all sheets
candidate_labels = df['Categories'].tolist()

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")


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

def storeReading(jwToken, imageLink, text1, text2, text3, text4, text5):
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

    userID = decodeToken(jwToken)
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


#Returns JSON (CardID, imageLink, text1-5) tuple
def getRecentCards(jwtoken):
    userID = decodeToken(jwtoken)
    cardsData = {}
    for NumOfCard in range(1, 8):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        #get cards
        cards = list(cursor.execute("SELECT card1, card2, card3, card4, card5, card6, card7 FROM users WHERE id = ?", (userID,)).fetchone())

        #get card's unique id 
        cardID = cards[NumOfCard - 1]
        if(cardID != 0):
            cardInfo = list(cursor.execute("SELECT * FROM cardReadings where id = ?", (cardID,)).fetchone())
            obj = {"id": cardInfo[0], "image": cardInfo[1], "text1": cardInfo[2], "text2": cardInfo[3], "text3": cardInfo[4], "text4": cardInfo[5], "text5": cardInfo[6]}
        else:
            obj = {"id": "-1", "image": "-1", "text1": "-1", "text2": "-1", "text3": "-1", "text4": "-1", "text5": "-1"}

        conn.close()

        cardsData[f"card{NumOfCard}"] = obj

    return cardsData


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

def getUserName(jwToken):
    secret_key = '589b1ea45ae4551b27639cdbdc6fc47d6c4e749ca9d45df423daafc592a623e2'
    try:
        decoded_payload = jwt.decode(jwToken, secret_key, algorithms='HS256')
        return decoded_payload['fname']
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
        retObject.set_cookie("auth",str(token),httponly=True, samesite="Lax")
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
        retObject.set_cookie("auth",str(token),httponly=True, samesite="Lax")
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
        #hits = random.choice(es.search(index="mtgcards", body={
            #"query": {"function_score": {"query": {"match_all": {}}, "random_score": {}}}})['hits']['hits'])
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

# @app.route('/getUserCards')
# def getUserCards():
#     

@app.route('/getcard/<query>',methods=['GET'])
def getcard(query):
    a = [x for x in re.compile('\w+').findall(query) if x not in bad_words]
    b = random.choice([searchCardsByName(k) for k in a])
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

# @app.route('/getcard',methods=['POST'])
# def getcard():
#     query = request.get_json()
#     b = searchCardsByName(query)
#     b = requests.get(b)
#     b.raise_for_status()
#     response = make_response(b.content)
#     image = Image.open(io.BytesIO(b.content))
#     width, height = image.size
#     left = 80 * width / 672
#     right = 592 * width / 672
#     top = 92 * height / 936
#     bottom = 500 * height / 936
#     img_byte_arr = io.BytesIO()
#     image.crop((left, top, right, bottom)).save(img_byte_arr, format='jpeg')
#     img_byte_arr = img_byte_arr.getvalue()
#     image.close()
#     response = make_response(img_byte_arr)
#     # this might be helpful
#     response.headers.set('Content-Type', 'image/jpeg')
#     # below will start a download
#     # response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % 'test')
#     return response

@app.route('/store_reading', methods=['OPTIONS'])
def handle_options():
    # Set CORS headers
    response = jsonify({'message': 'OPTIONS request handled successfully'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000') # Adjust this to your needs
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'PUT,POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')  # Allow credentials
    return response
@app.route('/store_reading', methods=['POST'])
def storeR():
    formData = request.get_json()
    jwToken = request.cookies.get('auth')
    print("post:{}".format(jwToken))
    title = formData['linkText'] # the question about the users day
    searchTxt = formData['imgText'] # image prompt
    modelOutput = findHoroscope(title,user=getUserName(jwToken))
    storeReading(jwToken, searchTxt, title, modelOutput,"","","")
    return getRecentCards(jwToken)

@app.route('/get_reading',methods=['GET'])
def getR():
    jwToken = request.cookies.get('auth')
    return getRecentCards(jwToken)

def findHoroscope(sequence_to_classify, number = 10, positivity_threshold = 2, positivity_weight = 2, power = 10, user="User"):
    c = classifier(sequence_to_classify, candidate_labels, multi_label=True)
    # c = {'sequence': 'blah', 'labels': ['a', 'b', 'c', 'd', 'e', 'f'], 'scores': [0.2,0.3,0,0.4,0.5,0.5]}
    c = pd.Series(index = c['labels'], data = c['scores']).sort_values(ascending=False) # .head(number).to_dict()
    print(c)
    a = 1
    var = 10000
    print(c.size)
    print(c.iloc[:a+2].std())
    print(c.iloc[a+1:].std())
    while a < c.size and c.iloc[:a+1].std() + c.iloc[a+1:].std() < var:
        var = c.iloc[:a+1].std() + c.iloc[a+1:].std()
        a += 1
        print(var)
        print(a)
    print(c.iloc[:a+1].std() + c.iloc[a+1:].std())
    c = c.head(a).to_dict()

    def get_list(label_noise):
        l = []
        for key in c:
            # l.append({"range": {key: {"gte": c[key]-label_noise,"lte": c[key]+label_noise}}})
            l.append({"range": {key: {"gte": c[key]-label_noise}}})
        return l
    # s = sentiment_pipeline(sequence_to_classify)
    # if s[0]['label'] == 'POSITIVE':
    #     print("Positive!")
    #     bad = 'negative'
    # else:
    #     print("Negative!")
    #     bad = 'positive'
    bad = 'positive'
    # hits = es.search(index="horoscopepredictedgeneral", body={"query": {"range": {bad: {"lte": 1000}},
    #                                                                                         }})['hits']['hits']
    # hits = es.search(index="horoscopepredictedgeneral", body={"query": {"bool": {"must": l}}})['hits']['hits']
    hits = []
    label_noise = 0.05
    while len(hits) < 10:
        hits = es.search(index="horoscopepredictedgeneral", body={"query": {"bool": {"must": get_list(label_noise)}}}, size= 100)['hits']['hits']
        label_noise += 0.05
    weights = [0] * len(hits)
    print(c)
    for i, j in enumerate(hits):
        print(j["_source"]["horoscope"])
        for k in c:
            print(float(j["_source"][k]))
            print(float(c[k]))
            weights[i] += (float(j["_source"][k])**power)*(float(c[k]))
    # print(weights)
    # print(hits)
    for i, a in enumerate(hits):
        print(weights[i])
        print(a["_source"]["horoscope"])
    # just weighting by the score
    hits = random.choices(hits, weights=weights, k=1)[0]
    # print(hits)
    # print(c)
    # print(s)
    return hits["_source"]["horoscope"].replace(hits["_source"]["sign"].lower().title(), user)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002,debug=False)
