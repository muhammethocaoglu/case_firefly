from rest_framework import serializers
from . import models
from customer_api.utilities import HashStringGenerator


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = HashStringGenerator.generate(validated_data['password'])
        return models.Customer.objects.create(**validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ('email', 'first_name', 'last_name')


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ('id', 'email', 'first_name', 'last_name')


class CustomerLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ('email', 'password')
