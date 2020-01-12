from customer_api.models import Customer
from rest_framework import generics, status
from rest_framework.response import Response

from customer_api.serializer import CustomerSerializer
from customer_api.serializer import CustomerListSerializer
from customer_api.serializer import CustomerLoginSerializer

import hashlib


class CustomerRegister(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        super(CustomerRegister, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)


class CustomerLogin(generics.GenericAPIView):
    serializer_class = CustomerLoginSerializer

    def post(self, request, *args, **kwargs):
        queryResultCustomerByEmail = Customer.objects.filter(email=request.data['email'])
        if not queryResultCustomerByEmail.exists():
            return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        customerPasswordHashed = queryResultCustomerByEmail[0].password

        encrypter = hashlib.md5()
        encrypter.update(request.data['password'].encode("utf-8"))
        passwordInRequestHashed = encrypter.hexdigest()

        if customerPasswordHashed != passwordInRequestHashed:
            return Response({"detail": "Customer is unauthorized."}, status=status.HTTP_401_UNAUTHORIZED)

        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully logged in"}
        return Response(response)


class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def retrieve(self, request, *args, **kwargs):
        super(CustomerDetail, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(CustomerDetail, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(CustomerDetail, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_204_NO_CONTENT,
                    "message": "Successfully deleted"}
        return Response(response)
