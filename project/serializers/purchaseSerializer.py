from rest_framework import serializers
from project.models import Purchase
from django.db import transaction
from django.contrib.auth.models import User
from django.db import IntegrityError
import time

from project.serializers.saleSerializer import generate_unique_sale_no


class UserSerializerDefault(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        

class PurchaseSerializer(serializers.ModelSerializer):
    user = UserSerializerDefault(read_only=True)
    class Meta:
        model = Purchase
        fields = '__all__' 
        read_only_fields = ['user','purchase_no', 'create_date']

    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    @transaction.atomic
    def create(self, validated_data):
        for _ in range(5):
            try:
                purchase_no = generate_unique_sale_no("PHNO", Purchase, 'purchase_no')
                validated_data['purchase_no'] = purchase_no
                sale = Purchase.objects.create(**validated_data)
                return sale
            except IntegrityError:
                time.sleep(0.1)
                continue

        raise IntegrityError("Failed to generate a unique sale number after multiple retries.")