"""
WSGI config for fintech project.

It exposes the WSGI callable as a module-level variable named ``application``.

# Quick-start development settings - unsuitable for production

# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

For more information on this file, see


# Quick-start development settings - unsuitable for production

# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# You'll have to do the following manually to clean this up:

#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True

#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
#from __future__ import unicode_literals



For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fintech.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
