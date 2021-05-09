from cryptography.fernet import Fernet, InvalidToken


class Encryp_Decryp:
    def __init__(self):
        pass

    def menu(self):
        while 1:
            print("-------------------------------------------------------------------")
            print("|             Please pick from the following options!             |")
            print("|             1.         Encrypt a file                           |")
            print("|             2.         Decrypt a file                           |")
            print("|             3.         Exit Encrypto                            |")
            print("-------------------------------------------------------------------")
            num = int(input())

            if num == 1:
                self.encrypto()
            elif num == 2:
                self.decrypto()
            else:
                break

    def encrypto(self):

        key = Fernet.generate_key()  # generates key to encrypt and saves to current directory
        key_file = open('key.key', 'wb')
        key_file.write(key)
        key_file.close()

        # getting input file to encrypt
        input_file = input("Please enter the file you'd like to encrypt: ")

        with open(input_file, 'rb') as file:
            file_info = file.read()

        key = Fernet(key)
        encrypted_file = key.encrypt(file_info)

        with open(input_file, 'wb') as file:
            file.write(encrypted_file)

    def decrypto(self):
        key_file = open('key.key', 'rb')       # reading the key that was used to encrypt
        key = key_file.read()
        key_file.close()

        input_file = input("Please enter the file you'd like to decrypt: ")

        with open(input_file, 'rb') as file:
            file_info = file.read()

        key = Fernet(key)

        try:

            decrypted_file = key.decrypt(file_info)

            with open(input_file, 'wb') as file:
                file.write(decrypted_file)

        except InvalidToken as e:

            print("Sorry, it looks like the key is invalid, please try again!")
