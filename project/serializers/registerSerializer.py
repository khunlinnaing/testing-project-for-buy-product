from rest_framework import serializers
from django.contrib.auth import get_user_model
from project.models import UserProfile
from django.contrib.auth.password_validation import validate_password
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    # Profile fields:
    phone = serializers.CharField(required=False, allow_blank=True)
    profile = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name',
                  'phone', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        profile_image = validated_data.pop('profile', None)

        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        print(user)
        print(phone)
        print(profile_image)

        UserProfile.objects.create(
            user=user,
            phone=phone,
            profile=profile_image
        )

        return user
