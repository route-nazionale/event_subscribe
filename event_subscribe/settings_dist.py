from default_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o*4+4o2wia&n8_i02q9rxhhyjzzb_ueqcn=y!(ws2-z7pgydoi'

DEBUG = True
TEMPLATE_DEBUG = True

# GOOGLE RECAPTCHA KEYS
RECAPTCHA_PUBLIC_KEY  = ''
RECAPTCHA_PRIVATE_KEY = ''

# CONTACT EMAIL FOR ERROR SUPPORT
SUPPORT_EMAIL = 'supporto@befair.it'

# IF REGISTRATION_OPEN == False, A MAINTENANCE VIEW IS SHOWED
REGISTRATIONS_OPEN = True

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'event_subscribe.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#        'LOCATION': 'cache_table',
#    }
#}

# tune as needed
CACHE_EXPIRE_TIME = 60 #seconds

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
