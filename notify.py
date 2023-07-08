import requests


def send_message(message:str, token:str, files={}):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': message}
    if files != None:
        files = {'imageFile': files}
    response = requests.post(url, headers=headers, data=data, files=files)
    if response.status_code == 200:
        print('Notification sent successfully!')
    else:
        print('Failed to send notification. Status code:', response.status_code)
