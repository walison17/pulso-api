import os

from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pulso.settings")

application = Sentry(get_wsgi_application())