"""
Django settings for gam_services project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import json
import dj_database_url

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Local
DEFAULT_CONNECTION = dj_database_url.parse(os.environ.get("DATABASE_URL"))

DATABASES = {
    'default': DEFAULT_CONNECTION
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'gam-manager-services.herokuapp.com',
    '127.0.0.1'
    ]

DFP = {
    'name': os.environ.get('DFP_NAME'),
    'email': os.environ.get('DFP_EMAIL'),
    'token_uri': json.loads(os.environ.get('DFP_TOKEN_URI')),
    'client_email': os.environ.get('DFP_EMAIL'),
    'private_key': json.loads(os.environ.get('DFP_PRIVATE_KEY')),
    'nw_code': os.environ.get('DFP_NWCODE'),
    'pk12': os.environ.get('DFP_PK12'),
}