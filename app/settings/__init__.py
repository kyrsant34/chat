import os

from .logging import logger
from .database import db

SALT = 'dc67e2549fa0485aa7da765f8b0585ae'
SECRET_KEY = os.getenv('SECRET_KEY', 'g9snkr*l#!7kv(d)ls62vamh1)v!c95o+ujxxxs-k^fb6t@kt*')
