import configparser
from libraries.database import PostgreSQL

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
    print(test.execute_query(sql)[0)

