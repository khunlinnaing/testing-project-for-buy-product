from rest_framework import serializers
from project.models import SaleProduct
from django.db import transaction
from project.serializers.generate_unique_key import generate_unique_sale_no
from project.serializers.purchaseSerializer import UserSerializerDefault
from django.db import IntegrityError
from django.db.models import Max
import time


class SaleSerializer(serializers.ModelSerializer):
    user = UserSerializerDefault(read_only=True)
    class Meta:
        model = SaleProduct
        fields = '__all__' 
        read_only_fields = ['user','sale_no', 'create_date']

    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    @transaction.atomic
    def create(self, validated_data):
        for _ in range(5):
            try:
                sale_no = generate_unique_sale_no("SANO", SaleProduct, 'sale_no')
                validated_data['sale_no'] = sale_no
                sale = SaleProduct.objects.create(**validated_data)
                return sale
            except IntegrityError:
                time.sleep(0.1)
                continue

        raise IntegrityError("Failed to generate a unique sale number after multiple retries.")

    
    