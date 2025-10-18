
# signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile_and_company(sender, instance, created, **kwargs):
    admin_username = getattr(settings, "ADMIN_USERNAME", None)
    admin_email = getattr(settings, "ADMIN_EMAIL", None)
    admin_password = getattr(settings, "ADMIN_PASSWORD", None)

    if admin_username and admin_password and not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email or "",
            password=admin_password
        )
        print(f"✅ Default admin user created: username={admin_username}")


    if created and instance.is_superuser:
        UserProfile.objects.create(user=instance)
