import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

SQ_BASE_URL = os.getenv('SQ_BASE_URL','https://dmeppiel.eu.ngrok.io/api')
SQ_TOKEN = os.getenv('SQ_TOKEN','b356ff9d8739d6c31cf4bee708d1d771756fa701')
PASSWORD_LENGTH = os.getenv('PASSWORD_LENGTH','6')