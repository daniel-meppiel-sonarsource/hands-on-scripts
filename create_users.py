import sys
import requests
import random
import string
import settings
from gsheets import GSheetsService

class UserCreationError(Exception):
    """A specific error"""
    pass

def get_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def get_request(endpoint):
    response = requests.get(settings.SQ_API_URL + '/' + endpoint, auth=(settings.SQ_TOKEN, ''))
    if not response.status_code == 200:
        print('Unexpected error ocurred, the request failed with HTTP code: {0}'.format(response.status_code))
        raise UserCreationError(response)
    return response

def post_request(endpoint, data):
    response = requests.post(settings.SQ_API_URL + '/' + endpoint, auth=(settings.SQ_TOKEN, ''), data = data)
    if not response.status_code == 200:
        print('Unexpected error ocurred, the request failed with HTTP code: {0}'.format(response.status_code))
        raise UserCreationError(response)
    return response

def create_users(num):
    users_dict = dict()
    for i in range(num):
        login = 'user_{}'.format(i)
        name = login
        password = get_random_string(int(settings.PASSWORD_LENGTH))
        print('Creating new user with login "{}"...'.format(login))
        post_request('users/create', {'login': login, 'name': name, 'password': password})
        users_dict[login] = password
    return users_dict

def search_user(login):
    return get_request('users/search?q={0}'.format(login))

def deactivate_users(num):
    for i in range(num):
        login = 'user_{}'.format(i)
        response = search_user(login)
        if not response.json()['users']:
            print("Stopping user deactivation: {0} was not found in SonarQube".format(login))
            break
        elif not response.json()['users'][0]['active']:
            print("Stopping user deactivation: {0} was already inactive".format(login))
            break
        print("Deactivating {0}...".format(login))
        post_request('users/deactivate', {'login': login,})


