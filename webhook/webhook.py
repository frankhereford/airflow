import json
import time
from flask import Flask, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.get_json()
    with open("/app/filename.txt", "w") as file:
        file.write("Webhook post\n")
        file.write("Current date and time: " + time.ctime() + "\n")
        file.write(json.dumps(payload))
        file.write("\n")
        file.flush()
    # Process the payload data here
    return 'Received webhook payload'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# here
