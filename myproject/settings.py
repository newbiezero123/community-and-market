
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s0yj7*9(j9+56om9ug98iay6i=hy6%t4xcsxwsxqogy#o$%@*o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
#192.168.1.191
#ipconfig
#ctr+r wf.msc
#python manage.py runserver 0.0.0.0:8000

#python manage.py runserver
#myenv\Scripts\activate
#http://127.0.0.1:8000/


# Application definition

INSTALLED_APPS = [
    # ก่อนอื่นให้เพิ่ม package ที่ใช้จัดการ admin interface:
    'admin_interface',
    'flat_responsive',
    # Package สำหรับจัดการสีใน admin:
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'widget_tweaks',
    'accounts',
    'posts',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_database',       # ชื่อฐานข้อมูลที่คุณสร้างใน PostgreSQL
        'USER': 'my_user',           # ชื่อผู้ใช้ใน PostgreSQL
        'PASSWORD': 'my_password',   # รหัสผ่านของผู้ใช้ใน PostgreSQL
        'HOST': 'localhost',         # โฮสต์ (ใช้ localhost หาก PostgreSQL อยู่ในเครื่องเดียวกัน)
        'PORT': '5432',              # พอร์ตเริ่มต้นของ PostgreSQL
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True
USE_TZ = True
USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  # โปรเจกต์หลัก
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# ตัวอย่างการตั้งค่าการปรับแต่ง django-admin-interface
X_FRAME_OPTIONS = 'SAMEORIGIN'

# ตั้งค่าสีพื้นหลังสำหรับ Admin
ADMIN_INTERFACE_THEME = 'dark'  # ตัวเลือก: 'dark' หรือ 'light'
