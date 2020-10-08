import requests

SQ_BASE_URL = 'https://dmeppiel.eu.ngrok.io/api'
SQ_TOKEN = 'b356ff9d8739d6c31cf4bee708d1d771756fa701'


def get_request(endpoint):
    return requests.get(SQ_BASE_URL + '/' + endpoint, auth=(SQ_TOKEN, ''))

def post_request(endpoint, data):
    return requests.post(SQ_BASE_URL + '/' + endpoint, auth=(SQ_TOKEN, ''), data = data)

def create_users(num):
    for i in range(num):
        login = 'user_{}'.format(i)
        name = login
        password = login
        post_request('users/create', {'login': login, 'name': name, 'password': password})

def deactivate_users(num):
    for i in range(num):
        login = 'user_{}'.format(i)
        post_request('users/deactivate', {'login': login,})

deactivate_users(2)