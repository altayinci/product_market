from rest_framework import serializers
from product_api.models import Product, DeliveryOptions


class DeliveryOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryOptions
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    delivery_options = DeliveryOptionsSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
