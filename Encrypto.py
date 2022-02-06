import eel
from cryptography.fernet import Fernet, InvalidToken
import sqlite3
import hashlib


eel.init("web")


@eel.expose
def new_db():
    with sqlite3.connect("Users.db") as db:
        cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(        
    username VARCHAR(20) NOT NULL ,
    hashcode VARCHAR(20) NOT NULL,   
    user_key VARCHAR(100) NOT NULL);

    ''')  # creates a database if there isn't already one existing


@eel.expose
def username_exists(username):
    with sqlite3.connect("Users.db") as db:
        cursor = db.cursor()
    findUser = ("SELECT * FROM user WHERE username = ?")
    cursor.execute(findUser, [(username)])
    if cursor.fetchall():
        return True
    else:
        return False


@eel.expose
def new_user(username, password):
    user_key = Fernet.generate_key()
    user_key = user_key.decode()

    hashingPass = hashlib.sha256(password.encode('utf-8'))
    hashcode = hashingPass.hexdigest()


    with sqlite3.connect("Users.db") as db:
        cursor = db.cursor()
    insertData = '''INSERT INTO user(username, hashcode, user_key)
        VALUES (?,?,?)'''
    cursor.execute(insertData, [(username), (hashcode), (user_key)])
    db.commit()

@eel.expose
def login(username, password):
    with sqlite3.connect("Users.db") as db:
        cursor = db.cursor()

    hashingPass = hashlib.sha256(password.encode('utf-8'))
    hashcode = hashingPass.hexdigest()

    find_user = ("SELECT * FROM user WHERE username = ? AND hashcode = ?")

    cursor.execute(find_user, [(username), (hashcode)])
    results = cursor.fetchone()

    if results:
        return True

    else:
        return False


@eel.expose
def get_key(username, password):
    with sqlite3.connect("Users.db") as db:
        cursor = db.cursor()

    hashingPass = hashlib.sha256(password.encode('utf-8'))
    hashcode = hashingPass.hexdigest()

    find_key = ('''SELECT user_key
                   FROM user
                   WHERE username == (?) AND hashcode == (?) 
    ''')

    cursor.execute(find_key, (username, hashcode))
    user_key = cursor.fetchone()
    return user_key[0]


@eel.expose
def encrypto(input_file, user_key):
    try:
        with open(input_file, 'rb') as file:
            file_info = file.read()

        user_key = Fernet(user_key)
        encrypted_file = user_key.encrypt(file_info)

        with open(input_file, 'wb') as file:
            file.write(encrypted_file)
        return True

    except IOError:
        return False


@eel.expose
def decrypto(input_file, user_key):
    user_key = Fernet(user_key)
    try:
        with open(input_file, 'rb') as file:
            file_info = file.read()

    except IOError:
        return False

    try:
        decrypted_file = user_key.decrypt(file_info)

        with open(input_file, 'wb') as file:
            file.write(decrypted_file)

    except InvalidToken as e:

        return False

    return True


eel.start("home.html", size=(1500, 800))
