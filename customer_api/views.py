from customer_api.models import Customer
from rest_framework import generics, status
from rest_framework.response import Response

from customer_api.serializer import CustomerSerializer
from customer_api.serializer import CustomerListSerializer
from customer_api.serializer import CustomerLoginSerializer
from customer_api.serializer import CustomerRegisterSerializer

import hashlib


def retrieve_customer_by_email(given_email):
    try:
        customer = Customer.objects.get(email=given_email)
    except Customer.DoesNotExist:
        customer = None
    return customer


def generate_response(status_code, message, result):
    response = {"status_code": status_code,
                "message": message,
                "result": result}
    return Response(response)


def generate_response_wout_result(status_code, message):
    response = {"status_code": status_code,
                "message": message}
    return Response(response)


class CustomerRegister(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer

    def create(self, request, *args, **kwargs):
        retrieved_customer = retrieve_customer_by_email(request.data['email'])
        if retrieved_customer is not None:
            return generate_response_wout_result(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                 'Customer with email -{}- already exists'.format(request.data['email']))
        initial_response = super(CustomerRegister, self).create(request, args, kwargs)
        return generate_response(initial_response.status_code, "Successfully created",
                                 {"id": initial_response.data['id'],
                                  "email": initial_response.data['email'],
                                  "first_name": initial_response.data['first_name'],
                                  "last_name": initial_response.data['last_name']})


class CustomerLogin(generics.GenericAPIView):
    serializer_class = CustomerLoginSerializer

    def post(self, request, *args, **kwargs):
        query_result_customer_by_email = retrieve_customer_by_email(request.data['email'])
        if query_result_customer_by_email is None:
            return generate_response_wout_result(status.HTTP_404_NOT_FOUND,
                                                 'Customer with email -{}- not found'.format(request.data['email']))
        customer_password_hashed = query_result_customer_by_email.password

        encryptor = hashlib.md5()
        encryptor.update(request.data['password'].encode("utf-8"))
        password_in_request_hashed = encryptor.hexdigest()

        if customer_password_hashed != password_in_request_hashed:
            return generate_response_wout_result(status.HTTP_401_UNAUTHORIZED, "Wrong password!")

        return generate_response_wout_result(status.HTTP_200_OK, "Successfully logged in")


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
        return generate_response(status.HTTP_200_OK, "Successfully retrieved", data)

    def patch(self, request, *args, **kwargs):
        super(CustomerDetail, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return generate_response(status.HTTP_200_OK, "Successfully updated", data)

    def delete(self, request, *args, **kwargs):
        super(CustomerDetail, self).delete(request, args, kwargs)
        return generate_response_wout_result(status.HTTP_204_NO_CONTENT, "Successfully deleted")
