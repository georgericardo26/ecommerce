from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'ecommerce',
        'PASSWORD': '',
        'HOST': 'ecommerce_db',
        'PORT': 5432
    }
}
