from .base import *

DEBUG = False

WSGI_APPLICATION = 'ecommerce.wsgi_prod.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'ecommerce',
        'PASSWORD': '',
        'HOST': 'ecommerce_db',
        'PORT': 5432
    }
}
