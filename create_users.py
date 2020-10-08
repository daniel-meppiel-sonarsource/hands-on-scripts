import sys
import requests
import random
import string
from gsheets import GSheetsService

SQ_BASE_URL = 'https://dmeppiel.eu.ngrok.io/api'
SQ_TOKEN = 'b356ff9d8739d6c31cf4bee708d1d771756fa701'

PASSWORD_LENGTH = 6

class UserCreationError(Exception):
    """A specific error"""
    pass

def get_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def get_request(endpoint):
    return requests.get(SQ_BASE_URL + '/' + endpoint, auth=(SQ_TOKEN, ''))

def post_request(endpoint, data):
    return requests.post(SQ_BASE_URL + '/' + endpoint, auth=(SQ_TOKEN, ''), data = data)

def create_users(num):
    users_dict = dict()
    for i in range(num):
        login = 'user_{}'.format(i)
        name = login
        password = get_random_string(PASSWORD_LENGTH)
        print('Creating new user with login "{}"...'.format(login))
        response = post_request('users/create', {'login': login, 'name': name, 'password': password})
        if not response.status_code == 200:
            print('Unexpected error ocurred while creating a new user: {0}'.format(response.text))
            raise UserCreationError(response.text)
        users_dict[login] = password
    return users_dict

def search_user(login):
    return get_request('users/search?q={0}'.format(login))

def deactivate_users(num):
    for i in range(num):
        login = 'user_{}'.format(i)
        response = search_user(login)
        if not response.status_code == 200:
            print('An unexpected error ocurred: {0}'.format(response.text))
            break
        elif not response.json()['users']:
            print("Stopping user deactivation: {0} was not found in SonarQube".format(login))
            break
        elif not response.json()['users'][0]['active']:
            print("Stopping user deactivation: {0} was already inactive".format(login))
            break
        print("Deactivating {0}...".format(login))
        response = post_request('users/deactivate', {'login': login,})
        if not response.status_code == 200:
            print('An unexpected error ocurred:{0}'.format(response.text))
            break
            

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("hands-on-user-creation")
    parser.add_argument("--delete", help='Will delete all hands-on exercise related users on the SonarQube server.', action='store_true')
    parser.add_argument("--num", help='Number of users to create when --delete flag is not present. Default value is 30.', type=int, action='store', default=30)
    parser.add_argument("--title", help='Name of the new Google Spreadsheet that will be created and written with the newly created user credentials, when the --delete flag is not present. Default is "Hands-On Exercises User List"', action='store', default='Hands-On Exercises User List')
    args = parser.parse_args()

    if not args.delete:
        print('Creating {} new SonarQube users...'.format(args.num))
        users = create_users(args.num)

        gsheetService = GSheetsService()
        print('Creating a new Google Spreadsheet titled {}...'.format(args.title))
        gsheetService.create(args.title)
        print('Writting user credential list to the new Google Spreadsheet...')
        gsheetService.write_users(users)
        print('EXECUTION SUCCESS')
    else:
        print('Deactivating all users with a login matching pattern "user_X"...')
        deactivate_users(args.num)


