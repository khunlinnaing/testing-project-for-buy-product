from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True, help_text="Username or Email")
    password = serializers.CharField(required=True, write_only=True, help_text="Password")

    def validate(self, attrs):
        username_or_email = attrs.get('identifier')
        password = attrs.get('password')

        user = self._authenticate(username_or_email, password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        attrs['user'] = user
        return attrs

    def _authenticate(self, username_or_email, password):
        # Try username
        user = authenticate(username=username_or_email, password=password)
        if user:
            return user

        # Try email
        try:
            user_obj = User.objects.get(email=username_or_email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        return user