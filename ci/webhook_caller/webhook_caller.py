import requests
import json

webhook_url = 'https://webhook.airflow.fyi/webhook'

payload = {
    'event_type': 'order_placed',
    'order_id': 12345,
    'customer_name': 'John Doe',
    'total_price': 99.99
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    print('Webhook called successfully')
else:
    print(f'Webhook call failed with status code {response.status_code}')
