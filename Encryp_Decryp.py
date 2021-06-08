import time

from cryptography.fernet import Fernet, InvalidToken
import sqlite3


class Encryp_Decryp:

    def __init__(self):
        with sqlite3.connect("Users.db") as db:
            cursor = db.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user(        
        username VARCHAR(20) NOT NULL ,
        password VARCHAR(20) NOT NULL,   
        user_key VARCHAR(100) NOT NULL);

        ''')  # creates a database if there isn't already one existing

    def user_menu(self):
        print("-------------------------------------------------------------------")
        print("|             Please Pick an Option Below                         |")
        print("|             1.         Create New User                          |")
        print("|             2.         Login                                    |")
        print("-------------------------------------------------------------------")
        num = int(input())

        if num == 1:
            self.new_user()
        elif num == 2:
            self.login()
        else:
            print("Invalid Input, please try again")
            self.user_menu()

    def encryp_menu(self, user_key):
        while 1:
            print("-------------------------------------------------------------------")
            print("|             Please Pick an Option Below                         |")
            print("|             1.         Encrypt File                             |")
            print("|             2.         Decrypt File                             |")
            print("|             3.         Exit                                     |")
            print("-------------------------------------------------------------------")
            num = int(input())
            if num == 1:
                self.encrypto(user_key)
            elif num == 2:
                self.decrypto(user_key)
            elif num == 3:
                print("Have a nice day :)")
                time.sleep(1)
                break
            else:
                print("Invalid Input, please try again")
                self.user_menu()

    def new_user(self):
        found = 0
        while found == 0:
            username = input("Please enter a username: ")
            with sqlite3.connect("Users.db") as db:
                cursor = db.cursor()
            findUser = ("SELECT * FROM user WHERE username = ?")
            cursor.execute(findUser, [(username)])

            if cursor.fetchall():
                print("Username has already been taken, please try again")
            else:
                found = 1

        user_key = Fernet.generate_key()
        user_key = user_key.decode()
        password = input("Enter password: ")
        password1 = input("Please enter password again: ")

        while password != password1:
            print("Your passwords don't match sorry, please try again ")
            password = input("Enter password: ")
            password1 = input("Please enter password again ")

        insertData = '''INSERT INTO user(username, password, user_key)
            VALUES (?,?,?)'''
        cursor.execute(insertData, [(username), (password), (user_key)])
        db.commit()

        self.encryp_menu(user_key)

    def login(self):
        username = input("Please enter username ")
        password = input("Please enter your password ")
        with sqlite3.connect("Users.db") as db:
            cursor = db.cursor()

        find_user = ("SELECT * FROM user WHERE username = ? AND password = ?")

        cursor.execute(find_user, [(username), (password)])
        results = cursor.fetchone()

        if results:
            print("Login Successful")
            user_key = self.get_key(username, password)
            self.encryp_menu(user_key)

        else:
            print("Username or password not recognized. This can happen if you're a new user.")
            again = input("Do you want to try again? Y or N -> ")
            if again.lower() == "n":
                print("Have a nice day :)")
                time.sleep(1)
                exit(0)
            elif again.lower() == "y":
                self.login()

    def get_key(self, username, password):
        with sqlite3.connect("Users.db") as db:
            cursor = db.cursor()

        find_key = ('''SELECT user_key
                       FROM user
                       WHERE username == (?) AND password == (?) 
        ''')

        cursor.execute(find_key, (username, password))
        user_key = cursor.fetchone()
        return user_key[0]

    def encrypto(self, user_key):
        # getting input file to encrypt
        input_file = input("Please enter the file you'd like to encrypt: ")

        try:
            with open(input_file, 'rb') as file:
                file_info = file.read()

            user_key = Fernet(user_key)
            encrypted_file = user_key.encrypt(file_info)

            with open(input_file, 'wb') as file:
                file.write(encrypted_file)

            print("File successfully encrypted!")

        except IOError:
            print("Sorry, looks like that file doesn't exist, please try again")

    def decrypto(self, user_key):
        input_file = input("Please enter the file you'd like to decrypt: ")

        user_key = Fernet(user_key)
        try:
            with open(input_file, 'rb') as file:
                file_info = file.read()

        except IOError:
            print("Sorry, looks like that file doesn't exist, please try again")
            self.encryp_menu()

        try:

            decrypted_file = user_key.decrypt(file_info)

            with open(input_file, 'wb') as file:
                file.write(decrypted_file)

        except InvalidToken as e:

            print("Sorry, it looks like the key is invalid. Please select another User")
            self.user_menu()

        print("File successfully decrypted!")
