from rest_framework import serializers
from . import models
import hashlib


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def create(self, validated_data):
        encrypter = hashlib.md5()
        encrypter.update(validated_data['password'].encode("utf-8"))
        passwordHash = encrypter.hexdigest()

        validated_data['password'] = passwordHash
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
