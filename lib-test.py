import configparser
from libraries.database import PostgreSQL
from libraries.security import Cryptography

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('app-config.ini')
    print(config['POSTGRES']['host'])

    db_config = dict(
        database=config['POSTGRES']['database'],
        host=config['POSTGRES']['host'],
        user=config['POSTGRES']['user'],
        password=config['POSTGRES']['password'],
        port=config['POSTGRES']['port'])

    test = PostgreSQL(db_config)

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
