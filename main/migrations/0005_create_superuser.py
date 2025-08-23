from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if username and email and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print("✅ Superuser created:", username)
        else:
            print("ℹ️ Superuser already exists:", username)
    else:
        print("⚠️ Superuser environment variables not set")

def delete_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    if username and User.objects.filter(username=username).exists():
        User.objects.filter(username=username).delete()
        print("🗑️ Superuser deleted:", username)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),  # replace with your actual first migration
    ]

    operations = [
        migrations.RunPython(create_superuser, delete_superuser),
    ]
