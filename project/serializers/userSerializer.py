from rest_framework import serializers
from django.contrib.auth.models import User
from project.models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'profile']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile_data = validated_data.get('profile', None)

        if profile_data:
            profile = instance.profile 
            profile.user=instance
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance
