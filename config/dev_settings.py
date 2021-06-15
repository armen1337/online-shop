from .base_settings import *


DEBUG = True


# DATABASES = {
#    'default':{
#       'ENGINE':'django.db.backends.postgresql_psycopg2',
#       'NAME':'online-shop',
#       'USER':'postgres',
#       'PASSWORD':'123456',
#       'HOST':'localhost',
#       'PORT':'5432',
#    }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}