from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username is None:
            username = kwargs.get('username')

        try:
            # Try to get user by username
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            try:
                # Try to get user by email
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
