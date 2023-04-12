## remember, this app doesn't need an API key, it needs a rate limiter.
## you can stay in sync with production all you want, just not too often.


import json
import time
from flask import Flask, request
import os, subprocess

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    os.chdir('/opt/airflow')
    environment = dict(os.environ)
    environment['GIT_SSH_COMMAND'] = 'ssh -i /opt/private_key_for_github -o IdentitiesOnly=yes -o "StrictHostKeyChecking=no"'
    data = subprocess.run(['git', 'pull'], env=environment, cwd=r'/opt/airflow', check=True, stdout=subprocess.PIPE).stdout
    print(data)
    return 'Received webhook payload'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
