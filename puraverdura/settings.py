"""
Django settings for puraverdura project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8cd-j&jo=-#ecd1jjulp_s*7y$n4tad(0d_g)l=6@n^r8fg3rn'

DEBUG = os.environ.get("JUNTAGRICO_DEBUG", 'True')=='True'

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
    'juntagrico',
    'impersonate',
    'crispy_forms',
    'puraverdura',
]

ROOT_URLCONF = 'puraverdura.urls'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('JUNTAGRICO_DATABASE_ENGINE','django.db.backends.sqlite3'), 
        'NAME': os.environ.get('JUNTAGRICO_DATABASE_NAME','puraverdura.db'), 
        'USER': os.environ.get('JUNTAGRICO_DATABASE_USER'), #''junatagrico', # The following settings are not used with sqlite3:
        'PASSWORD': os.environ.get('JUNTAGRICO_DATABASE_PASSWORD'), #''junatagrico',
        'HOST': os.environ.get('JUNTAGRICO_DATABASE_HOST'), #'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': os.environ.get('JUNTAGRICO_DATABASE_PORT', False), #''', # Set to empty string for default.
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
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
            'debug' : True
        },
    },
]

WSGI_APPLICATION = 'puraverdura.wsgi.application'


LANGUAGE_CODE = 'de-ch'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

DATE_INPUT_FORMATS =['%d.%m.%Y',]

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
    'impersonate.middleware.ImpersonateMiddleware'
]

EMAIL_HOST = os.environ.get('JUNTAGRICO_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('JUNTAGRICO_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('JUNTAGRICO_EMAIL_PASSWORD')
EMAIL_PORT = int(os.environ.get('JUNTAGRICO_EMAIL_PORT', '25' ))
EMAIL_USE_TLS = os.environ.get('JUNTAGRICO_EMAIL_TLS', 'False')=='True'
EMAIL_USE_SSL = os.environ.get('JUNTAGRICO_EMAIL_SSL', 'False')=='True'

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
            


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

IMPERSONATE = {
    'REDIRECT_URL': '/my/profile',
}

LOGIN_REDIRECT_URL = "/my/home"

"""
    File & Storage Settings
"""
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

MEDIA_ROOT = 'media'

"""
     Crispy Settings
"""
CRISPY_TEMPLATE_PACK = 'bootstrap4'

"""
     juntagrico Settings
"""
VOCABULARY = {
    'member': 'Mitglied',
    'member_pl' : 'Mitglieder',
    'assignment' : 'Arbeitseinsatz',
    'assignment_pl' : 'Arbeitseinsätze',
    'share' : 'Anteilschein',
    'share_pl' : 'Anteilscheine',
    'subscription' : 'Ernteanteil',
    'subscription_pl' : 'Ernteanteile',
    'co_member' : 'Mitabonnent',
    'co_member_pl' : 'Mitabonnenten',
    'price' : 'Jahresbeitrag',
    'member_type' : 'Mitglied',
    'member_type_pl' : 'Mitglieder',
    'depot' : 'Depot',
    'depot_pl' : 'Depots'
}
ORGANISATION_NAME = "Pura Verdura"
ORGANISATION_NAME_CONFIG = {"type" : "",
    "gender" : ""}
ORGANISATION_LONG_NAME = "Pura Verdura"
ORGANISATION_ADDRESS = {"name":"Pura Verdura", 
            "street" : "Drusbergstrasse",
            "number" : "113",
            "zip" : "8053",
            "city" : "Zürich",
            "extra" : "CH"}
ORGANISATION_PHONE =''
ORGANISATION_BANK_CONNECTION = {"PC" : "",
            "IBAN" : "CH38 0839 0036 8201 1000 0",
            "BIC" : "ABSOCH22XXX",
            "NAME" : "ABS",
            "ESR" : ""}
# INFO_EMAIL = "mitglieder@puraverdura.ch"
INFO_EMAIL = '"Pura Verdura" <mitglieder@puraverdura.ch>'
SERVER_URL = "www.puraverdura.ch"
ADMINPORTAL_NAME = "Mitgliederplattform Pura Verdura"
ADMINPORTAL_SERVER_URL = "login.puraverdura.ch"
BUSINESS_REGULATIONS = "https://www.puraverdura.ch/wp-content/uploads/20191025-Betriebsreglement-Pura-Verdura.pdf"
BYLAWS = "https://www.puraverdura.ch/wp-content/uploads/20191026_Final-nach-GV-Statuten_Pura-Verdura.pdf"
MAIL_TEMPLATE = "mails/email.html"
STYLE_SHEET = "/static/css/individual.css"
FAVICON = "/static/img/favicono.ico"
FAQ_DOC = "https://www.puraverdura.ch/faq/"
EXTRA_SUB_INFO = ""
ACTIVITY_AREA_INFO = ""
SHARE_PRICE = "500"
ENABLE_SHARES = True
BASE_FEE = ""
CURRENCY = "CHF"
ASSIGNMENT_UNIT = "ENTITY"
PROMOTED_JOB_TYPES = []
PROMOTED_JOBS_AMOUNT = 2
DEPOT_LIST_GENERATION_DAYS = [1,2,3,4,5,6,7]	
BILLING = False
BUSINESS_YEAR_START = {"day":1, "month":4}
BUSINESS_YEAR_CANCELATION_MONTH = 10
MEMBERSHIP_END_MONTH = 6
IMAGES = {'status_100': '/static/img/status_100_cropped.png',
            'status_75': '/static/img/status_75_cropped.png',
            'status_50': '/static/img/status_50_cropped.png',
            'status_25': '/static/img/status_25_cropped.png',
            'status_0': '/static/img/status_0_cropped.png',
            'single_full': '/static/img/schaufel_pickel_colored.png',
            'single_empty': '/static/img/schaufel_pickel_gray.png',
            'single_core': '/static/img/schaufel_pickel_colored.png',
            #'core': '/static/img/schaufel_iconized.png'}
            'core': '/static/img/Transparent_Pixel.png'}

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# EMAILS = {
#     'welcome': 'mails/welcome_mail.txt',
#     'co_welcome': 'mails/welcome_added_mail.txt',
#     'co_added': 'mails/added_mail.txt',
#     'password': 'mails/password_reset_mail.txt',
#     'j_reminder': 'mails/job_reminder_mail.txt',
#     'j_canceled': 'mails/job_canceled_mail.txt',
#     'confirm': 'mails/confirm.txt',
#     'j_changed': 'mails/job_time_changed_mail.txt',
#     'j_signup': 'mails/job_signup_mail.txt',
#     'd_changed': 'mails/depot_changed_mail.txt',
#     's_created': 'mails/share_created_mail.txt',
#     'n_sub': 'mails/new_subscription.txt',
#     's_canceled': 'mails/subscription_canceled_mail.txt',
#     'm_canceled': 'mails/membership_canceled_mail.txt',
#     'b_share': 'mails/bill_share.txt',
#     'b_sub': 'mails/bill_sub.txt',
#     'b_esub': 'mails/bill_extrasub.txt'
# }


EMAILS = {
    'welcome': 'puraverdura_emails/willkommen_mail.txt',
    'co_welcome': 'puraverdura_emails/mitabonnent_willkommen.txt',
    'confirm': 'mails/confirm.txt',
    's_created': 'puraverdura_emails/anteilsschein_mail.txt',
}
