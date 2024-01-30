from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import requests
from passlib.context import CryptContext
import secrets
import sqlite3
import User
import jwt

app = Flask(__name__)
CORS(app)



pwd_context = CryptContext(schemes=["sha256_crypt"])



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

@app.route('/')
def hello_world():
    return jsonify('Hello, World!')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002,debug=False)
