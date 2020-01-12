from customer_api.models import Customer
from rest_framework import generics, status
from django.http import Http404

from customer_api.serializer import CustomerSerializer
from customer_api.serializer import CustomerListSerializer
from customer_api.serializer import CustomerLoginSerializer
from customer_api.serializer import CustomerRegisterSerializer
from customer_api.utilities import ResponseGenerator
from customer_api.utilities import HashStringGenerator


def retrieve_customer_by_email(given_email):
    try:
        customer = Customer.objects.get(email=given_email)
    except Customer.DoesNotExist:
        customer = None
    return customer


class CustomerRegister(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer

    def create(self, request, *args, **kwargs):
        retrieved_customer = retrieve_customer_by_email(request.data['email'])
        if retrieved_customer is not None:
            return ResponseGenerator.generate_without_body(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                           'Customer with email {} already exists'.format(
                                                               request.data['email']))
        initial_response = super(CustomerRegister, self).create(request, args, kwargs)
        return ResponseGenerator.generate(initial_response.status_code, "Successfully created",
                                          {"id": initial_response.data['id'],
                                           "email": initial_response.data['email'],
                                           "first_name": initial_response.data['first_name'],
                                           "last_name": initial_response.data['last_name']})


class CustomerLogin(generics.GenericAPIView):
    serializer_class = CustomerLoginSerializer

    def post(self, request, *args, **kwargs):
        query_result_customer_by_email = retrieve_customer_by_email(request.data['email'])
        if query_result_customer_by_email is None:
            return ResponseGenerator.generate_without_body(status.HTTP_404_NOT_FOUND,
                                                           'Customer with email {} not found'.format(
                                                               request.data['email']))

        password_in_request_hashed = HashStringGenerator.generate(request.data['password'])
        if query_result_customer_by_email.password != password_in_request_hashed:
            return ResponseGenerator.generate_without_body(status.HTTP_401_UNAUTHORIZED, "Wrong password!")

        return ResponseGenerator.generate_without_body(status.HTTP_200_OK, "Successfully logged in")


class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            super(CustomerDetail, self).retrieve(request, args, kwargs)
        except Http404:
            return ResponseGenerator.generate_without_body(status.HTTP_404_NOT_FOUND,
                                                           'Customer with id {} not found'.format(kwargs['pk']))
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return ResponseGenerator.generate(status.HTTP_200_OK, "Successfully retrieved", data)

    def patch(self, request, *args, **kwargs):
        try:
            super(CustomerDetail, self).patch(request, args, kwargs)
        except Http404:
            return ResponseGenerator.generate_without_body(status.HTTP_404_NOT_FOUND,
                                                           'Customer with id {} not found'.format(kwargs['pk']))
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return ResponseGenerator.generate(status.HTTP_200_OK, "Successfully updated", data)

    def delete(self, request, *args, **kwargs):
        try:
            super(CustomerDetail, self).delete(request, args, kwargs)
        except Http404:
            return ResponseGenerator.generate_without_body(status.HTTP_404_NOT_FOUND,
                                                           'Customer with id {} not found'.format(kwargs['pk']))
        return ResponseGenerator.generate_without_body(status.HTTP_204_NO_CONTENT, "Successfully deleted")
