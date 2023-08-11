import configparser
import logging.handlers
import os
import sys

from flask import Flask, render_template, url_for, request, session, redirect
from libraries.respcode import *
from libraries.security import Cryptography
from libraries.database import PostgreSQL

app = Flask(__name__)
app.secret_key = os.urandom(24)

# initialize configuration file loading
try:
    db_config = {}
    config = configparser.ConfigParser()
    config.read('config/app-config.ini')

    if config.has_section('POSTGRES'):
        params = config.items('POSTGRES')
        for param in params:
            db_config[param[0]] = param[1]
    else:
        print("ERROR: Could not initialize database with provided configuration. Please check entries in app-config.ini.")
        sys.exit(0)
except FileNotFoundError as e:
    print("ERROR: Could not initialize configuration setup. Please check access to app-config.ini.")
    sys.exit(0)

# initialize logging handlers
try:
    log_file = config['LOG']['filename']
    logger = logging.getLogger('LOG')
    logger.setLevel(logging.INFO)
    rfh = logging.handlers.TimedRotatingFileHandler(filename=log_file, when='midnight')
    fmtr = logging.Formatter('%(asctime)s | %(message)s')
    rfh.setFormatter(fmtr)
    logger.addHandler(rfh)
except FileNotFoundError as e:
    print("ERROR: Could not initialize logging handlers. Please check if {} exist".format(log_file))
    sys.exit(0)

database = PostgreSQL(db_config)

@app.route('/')
def login():
    crypto = Cryptography()
    key = crypto.get_key()
    return render_template('login.htm', value=dict(stat=0, msg=""))

@app.route('/authenticate', methods=['POST'])
def authenticate_login():
    if request.method == 'POST':
        user  = request.form['uname']
        pword = request.form['pword']

        auth_sql = config['SQL']['auth'].format(user, pword)
        res = database.execute_query(auth_sql)

        if res[0] == SUCCESS:
            if res[1][0][0] < 1:
                val = dict(stat=1, msg=config['ERR']['inv_cred'])
            else:
                session['username'] = user
                last_login = config['SQL']['login'].format(user)
                database.execute_dml(last_login)

                render_template('home.htm')
        else:
            val = dict(stat=1, msg=config['ERR']['pg_error'].format(config['POSTGRES']['ip']))

    return render_template('login.htm', value=val)

@app.route('/logout', methods=['POST', 'GET'])
def terminate_login():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 5100
    logger.info("Running flask on {}:{}".format(ip, port))
    app.run(host=ip, port=port)
