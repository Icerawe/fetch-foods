import requests
import json


def send(message, token):

    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': message}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print('Notification sent successfully!')
    else:
        print('Failed to send notification. Status code:', response.status_code)
