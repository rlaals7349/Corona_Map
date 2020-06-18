"""
WSGI config for BusanCorona project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import os, sys
path = os.path.abspath(__file__+'/../..')
if path not in sys.path:
    sys.path.append(path)
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusanCorona.settings")
application = get_wsgi_application()

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BusanCorona.settings')

# application = get_wsgi_application()




