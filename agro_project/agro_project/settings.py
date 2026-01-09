
from pathlib import Path
import os
from decouple import config, Csv


BASE_DIR = Path(__file__).resolve().parent.parent







SECRET_KEY = config('SECRET_KEY', default='django-insecure-w2@bc3td1l=nr-!3s5ei7ug_kse$0@i7zg1qc=6c53vl05*m4o')


DEBUG = True

ALLOWED_HOSTS = []




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'farmers_app',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'agro_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'agro_project.wsgi.application'





DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}





AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]





LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True





STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


MONGODB_SETTINGS = {
    'host': config('MONGODB_HOST', default='mongodb://localhost:27017/'),
    'db': config('MONGODB_DB', default='agro-db'),
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False





WHISPER_MODEL_SIZE = config('WHISPER_MODEL_SIZE', default='small')



OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY', default='8e5d12c1be071988df6887ba71ae6aa0')
OPENWEATHER_API_URL = config('OPENWEATHER_API_URL', default='https://api.openweathermap.org/data/2.5/weather')
OPENWEATHER_ONECALL_URL = config('OPENWEATHER_ONECALL_URL', default='https://api.openweathermap.org/data/3.0/onecall')



RAG_MODEL_WEBHOOK_URL = config('RAG_MODEL_WEBHOOK_URL', default='')
RAG_MODEL_API_KEY = config('RAG_MODEL_API_KEY', default='')




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'