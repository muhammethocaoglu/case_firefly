from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Customer
from .serializer import CustomerSerializer


# Create your views here.


class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
