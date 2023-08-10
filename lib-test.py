import configparser
from libraries.database import PostgreSQL
from libraries.security import Cryptography

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('app-config.ini')
    print(config['POSTGRES']['ip'])

    test = PostgreSQL(
        config['POSTGRES']['dbname'],
        config['POSTGRES']['ip'],
        config['POSTGRES']['username'],
        config['POSTGRES']['password'],
        config['POSTGRES']['port'])
    sql = "select * from users"
    print(test.execute_query(sql)[1])

    # test Cryptography class
    c = Cryptography()
    ipass = "Test123$$"
    x = c.encrypt(ipass)

    print("{} encrypted is >> {}".format(ipass, x))
    key = c.get_key()

    c1 = Cryptography(key)
    y = c1.decrypt(x)
    print("Decrypted >> {}".format(y))
