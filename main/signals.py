from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
import os

def create_superuser(sender, **kwargs):
    User = get_user_model()
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if username and email and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print("✅ Superuser created")
        else:
            print("ℹ️ Superuser already exists")

post_migrate.connect(create_superuser)
