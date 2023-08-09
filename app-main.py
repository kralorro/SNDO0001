import os
import configparser
import logging.handlers
import sys

from flask import Flask, render_template, url_for
from libraries.security import Cryptography
from libraries.database import PostgreSQL

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('app-config.ini')

try:
    log_file = config['LOG']['filename']
    logger = logging.getLogger('LOG')
    logger.setLevel(logging.INFO)
    rfh = logging.handlers.TimedRotatingFileHandler(filename=log_file, when='midnight')
    fmtr = logging.Formatter('%(asctime)s | %(message)s')
    rfh.setFormatter(fmtr)
    logger.addHandler(rfh)

except FileNotFoundError as e:
    print("ERROR: Could not initialize logging handlers.")
    sys.exit(0)


database = PostgreSQL(
    config['POSTGRES']['dbname'],
    config['POSTGRES']['ip'],
    config['POSTGRES']['username'],
    config['POSTGRES']['password'],
    config['POSTGRES']['port'])

@app.route('/')
def login():
    crypto = Cryptography()
    key = crypto.get_key()
    return render_template('login.htm', value={'key': key})

@app.route('/authenticate', methods=['POST'])
def authenticate_login():
    pass

@app.route('/logout', methods=['POST', 'GET'])
def terminate_login():
    pass


if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 5100
    logger.info("Running flask on {}:{}".format(ip, port))
    app.run(host=ip, port=port)