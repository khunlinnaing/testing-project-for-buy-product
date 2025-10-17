# project/serializers.py
from rest_framework import serializers
from project.models import WorkLog

class WorkLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkLog
        # exclude = ["date"]
        fields = '__all__'

    def create(self, validated_data):
        """
        If a WorkLog with the same user and date exists, update it.
        Otherwise, create a new one.
        """
        user = validated_data.get('user')
        date = validated_data.get('date')
        instance, created = WorkLog.objects.update_or_create(
            user=user,
            date=date,
            defaults=validated_data
        )
        return instance

