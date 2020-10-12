import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

SQ_URL = os.getenv('SQ_URL','https://dmeppiel.eu.ngrok.io/')
SQ_URL = SQ_URL if SQ_URL.endswith('/') else SQ_URL + '/'
SQ_API_URL = SQ_URL + 'api'
SQ_TOKEN = os.getenv('SQ_TOKEN','e024fa8a672aaf5010bbe89d5ba3e95901316b2c')
GROUP_NAME = os.getenv('GROUP_NAME','training-users')
PASSWORD_LENGTH = os.getenv('PASSWORD_LENGTH','6')