import os,sys

pwd=os.path.dirname(os.path.dirname(os.path.realpath("__file__")))
sys.path.append(pwd+"../"+"../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mxshop.settings')

import django
django.setup()

from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User=get_user_model()
user=User.objects.all()
token=Token.objects.create(user=user[0])