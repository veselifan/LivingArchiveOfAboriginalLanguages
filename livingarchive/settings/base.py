"""
Django settings for livingarchive project.

Generated by 'django-admin startproject' using Django 3.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from dotenv import load_dotenv
load_dotenv()


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

PASSWORD_REQUIRED_TEMPLATE = 'password_required.html'

api_key=str(os.getenv("API_KEY"))

WAGTAIL_ADDRESS_MAP_CENTER = 'Australia'  # It must be a properly formatted address
WAGTAIL_ADDRESS_MAP_KEY = str(api_key)
GOOGLE_MAPS_V3_APIKEY = str(api_key)
GEO_WIDGET_DEFAULT_LOCATION = {'lat': -23.91276975, 'lng': 134.260923}

#WAGTAIL_VIDEOS_DISABLE_TRANSCODE = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',
    'wagtailgmaps',
    'blog',
    # 'wagtail',
    'wagtailvideos',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'captcha',
    'wagtailmenus',
    'user_group_management',
    'wagtailstreamforms',
    'modelcluster',
    'taggit',
    'allauth',
    'allauth.account',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'allauth.socialaccount',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'livingarchive',
    'wagtailmedia',
    'wagtail_pdf_view',
    'wagtailgeowidget'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'livingarchive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
                   
        'libraries':{
            'templatetag': 'blog.templatetags.to_at',
            
            }
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]

WSGI_APPLICATION = 'livingarchive.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(PROJECT_DIR, '../blog/static'),
]
FILE_UPLOAD_TEMP_DIR = str(os.path.join(PROJECT_DIR, 'tmp'))

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/livingarchive/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "livingarchive"
WAGTAIL_CACHE="False"
# Search
# https://docs.wagtail.io/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'filters': {
   'require_debug_false': {
       '()': 'django.utils.log.RequireDebugFalse',
   },
},
'formatters': {
   'verbose': {
       'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
       'datefmt': "%d/%b/%Y %H:%M:%S"
   },
   'simple': {
       'format': '%(levelname)s %(message)s'
   },
},
'handlers': {
   'file': {
       'level': 'ERROR',
       'filters': ['require_debug_false'],
       'class': 'logging.FileHandler',
      # 'filename': os.path.join(ev('APP_LOG_DIR'), "debug.log"),
       'filename': "./debug.log",
       "formatter": "verbose",
   },
},
'loggers': {
   'django': {
       'handlers': ['file'],
       'level': 'ERROR',
       'propagate': True,
   },
   'django.request': {
       'handlers': ['file'],
       'level': 'ERROR',
       'propagate': True,
   },
   'django.server': {
       'handlers': ['file',],
       'level': 'ERROR',
       'propagate': True,
   },
},
}
# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://indigenousengineering.org.au'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_BLACKLIST = ["admin","moderator","editor"]
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_SIGNUP_FORM_CLASS = 'livingarchive.forms.LocalSignupForm'
RECAPTCHA_PUBLIC_KEY = "6LdIMWMmAAAAAF5D0LJkeFzjSqOU14B5H4FZHgVw"
RECAPTCHA_PRIVATE_KEY = "6LdIMWMmAAAAADhhq-Moc6CePI9S_rVhpK0YegWB"

#RECAPTCHA_PUBLIC_KEY = "6Lcq534jAAAAAI9rFdVDOopTwSp92z9dox_FEEj1"
#RECAPTCHA_PRIVATE_KEY = "6Lcq534jAAAAAGcusv7gqVgT1vMY6CCaBJmkBE-A"

#RECAPTCHA_PUBLIC_KEY = "6LfsIJYjAAAAAMOjW3Ysb4IdNQyxRatxcu1PmavL"
#RECAPTCHA_PRIVATE_KEY = "6LfsIJYjAAAAAJMlLIzgjkOXPAdnqffi1syvL3o2"

NOCAPTCHA = True
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# wagtail media settings

WAGTAILMEDIA = {
    "MEDIA_MODEL": "wagtailmedia.Media",  # string, dotted-notation.
    "MEDIA_FORM_BASE": "",  # string, dotted-notation. Defaults to an empty string
    "AUDIO_EXTENSIONS": [
        "aac",
        "aiff",
        "flac",
        "m4a",
        "m4b",
        "mp3",
        "ogg",
        "wav",
    ],  # list of extensions
    "VIDEO_EXTENSIONS": [
        "avi",
        "h264",
        "m4v",
        "mkv",
        "mov",
        "mp4",
        "mpeg",
        "mpg",
        "ogv",
        "webm",
    ],  # list of extensions
}

X_FRAME_OPTIONS = 'SAMEORIGIN'
