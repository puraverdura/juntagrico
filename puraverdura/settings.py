"""
Django settings for puraverdura project.
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('JUNTAGRICO_SECRET_KEY')
# SECRET_KEY = 'fake-key'
DEBUG = os.environ.get("JUNTAGRICO_DEBUG", 'False')=='True'
# DEBUG = True

ALLOWED_HOSTS = ['login.puraverdura.ch','puraverdura.juntagrico.science', 'localhost',]


# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'polymorphic',
    'django_admin_shell',
    'juntagrico',
    'juntagrico_badges',
    'impersonate',
    'crispy_forms',
    'puraverdura',
    'adminsortable2',
    'juntagrico_pg'
]

ROOT_URLCONF = 'puraverdura.urls'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('JUNTAGRICO_DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('JUNTAGRICO_DATABASE_NAME', 'puraverdura.db'),
        'USER': os.environ.get('JUNTAGRICO_DATABASE_USER'),
        # ''junatagrico', # The following settings are not used with sqlite3:
        'PASSWORD': os.environ.get('JUNTAGRICO_DATABASE_PASSWORD'),  # ''junatagrico',
        'HOST': os.environ.get('JUNTAGRICO_DATABASE_HOST'),
        # 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': os.environ.get('JUNTAGRICO_DATABASE_PORT', False),  # ''', # Set to empty string for default.
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
            'debug': True
        },
    },
]

WSGI_APPLICATION = 'puraverdura.wsgi.application'

LANGUAGE_CODE = 'de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Change maximum number of allowed fields (default: 1000)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000

USE_TZ = True
TIME_ZONE = 'Europe/Zurich'

DATE_INPUT_FORMATS = ['%d.%m.%Y', ]

AUTHENTICATION_BACKENDS = (
    'juntagrico.util.auth.AuthenticateWithEmail',
    'django.contrib.auth.backends.ModelBackend'
)

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware'
]

EMAIL_HOST = os.environ.get('JUNTAGRICO_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('JUNTAGRICO_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('JUNTAGRICO_EMAIL_PASSWORD')
EMAIL_PORT = int(os.environ.get('JUNTAGRICO_EMAIL_PORT', '25'))
EMAIL_USE_TLS = os.environ.get('JUNTAGRICO_EMAIL_TLS', 'False') == 'True'
EMAIL_USE_SSL = os.environ.get('JUNTAGRICO_EMAIL_SSL', 'False') == 'True'

FROM_FILTER = {
    # This regex matches @puraverdura.ch email addresses, standalone or in "Name" <email> format.
    'filter_expression': '(?:\"[A-Za-zÄäÖöÜüß0-9._%+\s-]+\" )?<([A-Za-z0-9._%+-]+@puraverdura\.ch)>|[A-Za-z0-9._%+-]+@puraverdura\.ch',
    'replacement_from': '"Pura Verdura Mitglied" <server@puraverdura.ch>'
}

ADMINS = (
    ('Admin', os.environ.get('JUNTAGRICO_ADMIN_EMAIL')),
)

DEFAULT_MAILER = 'juntagrico.util.mailer.batch.Mailer'
BATCH_MAILER = {
    'batch_size': 39,
    'wait_time': 65
}

DEFAULT_FROM_EMAIL = 'it@puraverdura.ch'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

WHITELIST_EMAILS = []


def whitelist_email_from_env(var_env_name):
    email = os.environ.get(var_env_name)
    if email:
        WHITELIST_EMAILS.append(email.replace('@gmail.com', '(\+\S+)?@gmail.com'))


if DEBUG is True:
    for key in os.environ.keys():
        if key.startswith("JUNTAGRICO_EMAIL_WHITELISTED"):
            whitelist_email_from_env(key)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

IMPERSONATE = {
    'REDIRECT_URL': '/my/profile',
}

LOGIN_REDIRECT_URL = "/my/home"

# File & Storage Settings
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
MEDIA_ROOT = 'media'

# Crispy Settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# juntagrico Settings
VOCABULARY = {
    'member': 'Mitglied',
    'member_pl': 'Mitglieder',
    'assignment': 'Arbeitseinsatz',
    'assignment_pl': 'Arbeitseinsätze',
    'share': 'Anteilschein',
    'share_pl': 'Anteilscheine',
    'subscription': 'Ernteanteil',
    'subscription_pl': 'Ernteanteile',
    'co_member': 'Mitabonnent',
    'co_member_pl': 'Mitabonnenten',
    'price': 'Jahresbeitrag',
    'member_type': 'Mitglied',
    'member_type_pl': 'Mitglieder',
    'depot': 'Depot',
    'depot_pl': 'Depots',
}
ORGANISATION_NAME = "Pura Verdura"
ORGANISATION_NAME_CONFIG = {"type": "",
                            "gender": ""}
ORGANISATION_LONG_NAME = "Pura Verdura"
ORGANISATION_ADDRESS = {"name": "Genossenschaft Pura Verdura",
                        "street": "Drusbergstrasse",
                        "number": "113",
                        "zip": "8053",
                        "city": "Zürich",
                        "extra": ""}
ORGANISATION_PHONE = ''
ORGANISATION_BANK_CONNECTION = {"PC": "46-110-7",
                                "IBAN": "CH38 0839 0036 8201 1000 0",
                                "BIC": "ABSOCH22XXX",
                                "NAME": "ABS",
                                "ESR": ""}

INFO_EMAIL = '"Pura Verdura" <mitglieder@puraverdura.ch>'
SERVER_URL = "www.puraverdura.ch"
BUSINESS_REGULATIONS = "https://wordpress.puraverdura.ch/wp-content/uploads/20210720_Betriebsreglement.pdf"
BYLAWS = "https://wordpress.puraverdura.ch/wp-content/uploads/Statuten_Pura-Verdura_Version_2022_nach-GV.pdf"
MAIL_TEMPLATE = "mails/email.html"
STYLES = {'static': ['css/individual.css']}
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
FAVICON = "/static/img/favicono.ico"
EXTRA_SUB_INFO = ""
ACTIVITY_AREA_INFO = ""
SHARE_PRICE = "500"
ENABLE_SHARES = True
BASE_FEE = ""
CURRENCY = "CHF"
ASSIGNMENT_UNIT = "ENTITY"
PROMOTED_JOB_TYPES = []
PROMOTED_JOBS_AMOUNT = 2
DEPOT_LIST_GENERATION_DAYS = [1, 2, 3, 4, 5, 6, 7]
BILLING = False
BUSINESS_YEAR_START = {"day": 1, "month": 4}
BUSINESS_YEAR_CANCELATION_MONTH = 12
MEMBERSHIP_END_MONTH = 12
USE_JOB_STATUS_IMAGES = True
IMAGES = {'status_100': '/static/img/status_100_cropped.png',
          'status_75': '/static/img/status_75_cropped.png',
          'status_50': '/static/img/status_50_cropped.png',
          'status_25': '/static/img/status_25_cropped.png',
          'status_0': '/static/img/status_0_cropped.png',
          'single_full': '/static/img/schaufel_pickel_colored.png',
          'single_empty': '/static/img/schaufel_pickel_gray.png',
          'single_core': '/static/img/schaufel_pickel_colored.png',
          'core': '/static/img/samen_iconized.png'}

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

EMAILS = {
    'welcome': 'puraverdura_emails/willkommen_mail.txt',
    # 'welcome': 'puraverdura_emails/willkommen_mail_warteliste.txt',
    'co_welcome': 'puraverdura_emails/mitabonnent_willkommen.txt',
    's_created': 'puraverdura_emails/anteilsschein_mail.txt',
    # 's_created': 'puraverdura_emails/anteilsschein_mail_warteliste.txt',
    's_canceled': 'puraverdura_emails/subscription_canceled_mail.txt',
}

# Admin shell
ADMIN_SHELL_ONLY_DEBUG_MODE = True
