from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', 'social_db'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'psql'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}