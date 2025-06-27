"""
WSGI config for fooddelivery project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fooddelivery.settings')

application = get_wsgi_application()
