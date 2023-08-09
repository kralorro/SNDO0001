import os
from flask import Flask, render_template, url_for
from libraries.security import Cryptography

app = Flask(__name__)

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
    app.run()