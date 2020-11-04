import sys
import requests
import random
import string
import settings
from gsheets import GSheetsService


class RequestError(Exception):
    """A specific error"""
    pass

class NotFoundError(Exception):
    """A specific error"""
    pass

class User(object):
    login = None
    password = None
    token = None

    def __init__(self, login, name = None, password = None):
        self.login = login
        self.name = login if not name else name
        self.password = get_random_string(int(settings.PASSWORD_LENGTH)) if not password else password
        post_request('users/create', {'login': self.login, 'name': self.name, 'password': self.password})

    def generate_token(self, name='Hands-On Exercises Token'):
        self.token = post_request('user_tokens/generate', {'login':self.login, 'name':name}).json()['token']

    @staticmethod
    def deactivate(login):
        return post_request('users/deactivate', {'login': login,})

    @staticmethod
    def search(login):
        return get_request('users/search?q={0}'.format(login)).json()['users']


class Group(object):
    id = None
    name = None
    description = None

    def __init__(self, name, description = None):
        self.name = name
        self.description = description
        group_json = post_request('user_groups/create', {'name': self.name, 'description':self.description}).json()['group']
        self.id = group_json['id']

    def add_user(self, login):
        return post_request('user_groups/add_user', {'login': login, 'name':self.name})

    def add_permission(self, permission):
        return post_request('permissions/add_group', {'groupName': self.name, 'permission':permission})

    @staticmethod
    def delete(name):
        try:
            return post_request('user_groups/delete', {'name': name})
        except NotFoundError:
            print("Group {} was not found".format(name))


def get_request(endpoint):
    response = requests.get(settings.SQ_API_URL + '/' + endpoint, auth=(settings.SQ_TOKEN, ''))
    if response.status_code == 404:
        raise NotFoundError(response)
    elif not response.status_code == 200:
        print('Unexpected error ocurred, the request failed with HTTP code: {0}'.format(response.status_code))
        raise RequestError(response)
    return response

def post_request(endpoint, data):
    response = requests.post(settings.SQ_API_URL + '/' + endpoint, auth=(settings.SQ_TOKEN, ''), data = data)
    if response.status_code == 404:
        raise NotFoundError(response)
    elif not response.status_code == 200 and not response.status_code == 204:
        print('Unexpected error ocurred, the request failed with HTTP code: {0}'.format(response.status_code))
        raise RequestError(response)
    return response

def get_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def create_training_group():
    group = Group(settings.GROUP_NAME)
    group.add_permission('provisioning')
    group.add_permission('scan')
    group.add_permission('gateadmin')
    group.add_permission('profileadmin')
    return group

def create_users(num, group = None):
    users_list = list()
    for i in range(num):
        login = 'user_{}'.format(i)
        print('Creating new user with login "{}"...'.format(login))
        user = User(login)
        print('Generating token for user "{}"...'.format(login))
        user.generate_token()
        users_list.append(user)
        if group:
            print('Adding user "{}" to group "{}"...'.format(login, group.name))
            group.add_user(login)
    return users_list  

def deactivate_users(num):
    for i in range(num):
        login = 'user_{}'.format(i)
        users = User.search(login)
        if not users:
            print("Stopping user deactivation: {0} was not found in SonarQube".format(login))
            break
        elif not users[0]['active']:
            print("Stopping user deactivation: {0} was already inactive".format(login))
            break
        print("Deactivating {0}...".format(login))
        User.deactivate(login)


