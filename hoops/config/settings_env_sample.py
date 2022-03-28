# Rename this file to settings-[your env name].py   for example settings-prd.py 
# settings-*.py is in .gitignore so that your production settings dont get committed to GitHub.

from . settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['hoops.run']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hoops',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'db-name',
        'USER': 'db-user',
        'PASSWORD': 'db-pass',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {
            'sql_mode': 'traditional',
        }

    }
}

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')