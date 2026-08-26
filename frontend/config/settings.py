"""
Django settings for config project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-z@54pn!vh^t@9$q)!pp1w6dluuvibhq9)x85k!t$ndj27y4xw('

DEBUG = True

# Vercel sirve la app bajo un subdominio *.vercel.app. Se agregan
# localhost/127.0.0.1 para que también funcione en desarrollo local.
ALLOWED_HOSTS = [".vercel.app", "localhost", "127.0.0.1"]

# Necesario para que Django confíe en los POST (formularios con CSRF)
# que llegan por HTTPS a través de Vercel.
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]

# Vercel termina el TLS y reenvía la petición a Django marcándola con
# este header; sin esto Django cree que la conexión no es segura y
# puede rechazar el CSRF token del formulario.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tienda",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


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


MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# URL base del backend de FastAPI.
# - En local: por defecto usa uvicorn en tu máquina (puerto 8001).
# - En producción (Vercel): define la variable de entorno FASTAPI_URL
#   en el dashboard del proyecto de Vercel con el valor
#   "https://taller2-deploy-q01n.onrender.com" (tu API en Render),
#   así no hay que tocar este archivo para desplegar.
FASTAPI_URL = os.environ.get(
    "FASTAPI_URL",
    "http://127.0.0.1:8001",
)
