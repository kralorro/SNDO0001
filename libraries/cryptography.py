from cryptography.fernet import Fernet

class Cryptography:
    def __init__(self, key=False):
        self.__key = Fernet.generate_key() if key is False else key.encode('UTF-8')
        self.__cipher_suite = Fernet(self.__key)

    def get_key(self):
        return self.__key.decode('UTF=8')

    def encrypt(self, clear_text):
        return self.__cipher_suite.encrypt((clear_text).encode('UTF-8')).decode('UTF-8')

    def decrypt(self, cypher_text):
        return self.__cipher_suite.decrypt(cypher_text.encode('UTF-8')).decode('UTF-8')


if __name__ == "__main__":
    c = Cryptography()
    x = c.encrypt('Kent')

    print(x)
    key = c.get_key()

    c1 = Cryptography(key)
    y = c1.decrypt(x)
    print(y)