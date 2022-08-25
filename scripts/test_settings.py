from config.settings import DATABASES


SECRET_KEY = 'test'
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    # third party apps
    'django_extensions',
    'captcha',
    # local
    'contact.apps.ContactConfig',
    'analysis.apps.AnalysisConfig',
    'data_sourcing.apps.DataSourcingConfig',
    'predictions.apps.PredictionsConfig',
    'homepage.apps.HomepageConfig',
]