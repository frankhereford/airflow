from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.get_json()
    print(payload)
    # Process the payload data here
    return 'Received webhook payload'

if __name__ == '__main__':
    app.run(port=5000)
