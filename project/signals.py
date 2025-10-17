# signals.py

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile_and_company(sender, instance, created, **kwargs):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="admin"
        )
        print("✅ Default admin user created: username=admin, password=admin")
    if created and instance.is_superuser:
        UserProfile.objects.create(user=instance)
