"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os
from os.path import join,dirname,abspath
 
PROJECT_DIR = dirname(dirname(abspath(__file__)))
import sys 
sys.path.insert(0,PROJECT_DIR) 
#sys.path.append('/usr/lib/python3.4/site-packages')
#sys.path.append('/usr/lib64/python3.4/site-packages')
 
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

application = get_wsgi_application()
