import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from customer_api.models import Customer
from customer_api.serializer import CustomerSerializer
from customer_api.serializer import CustomerListSerializer
from customer_api.utilities import HashStringGenerator

client = Client()


class ListCustomersTest(TestCase):

    def setUp(self):
        Customer.objects.create(
            email='first@user.com', password='anyFirstPassword', first_name='anyFirstName', last_name='anyLastName')
        Customer.objects.create(
            email='second@user.com', password='anySecondPassword', first_name='secondFirstName',
            last_name='secondLastName')
        Customer.objects.create(
            email='third@user.com', password='anyThirdPassword', first_name='thirdFirstName', last_name='thirdLastName')
        Customer.objects.create(
            email='fourth@user.com', password='anyFourthPassword', first_name='fourthFirstName',
            last_name='fourthLastName')

    def should_list_customers(self):
        response = client.get(reverse('list_customers'))
        customers = Customer.objects.all()
        serializer = CustomerListSerializer(customers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RegisterCustomerTest(TestCase):

    def setUp(self):
        Customer.objects.create(
            email='first@user.com', password='anyFirstPassword', first_name='anyFirstName', last_name='anyLastName')

    def should_register_customer(self):
        response = self.client.post(reverse('register_customer'), {'email': 'any@mail.com', 'password': 'anyPass',
                                                                   'first_name': 'anyFirstName',
                                                                   'last_name': 'anyLastName'})
        customer = Customer.objects.get(email='any@mail.com')
        self.assertEqual(response.data['body']['email'], customer.email)
        self.assertEqual(response.data['body']['first_name'], customer.first_name)
        self.assertEqual(response.data['body']['last_name'], customer.last_name)
        self.assertEqual(response.data['status_code'], status.HTTP_201_CREATED)

    def should_return_error_when_register_customer_if_customer_already_exists(self):
        response = self.client.post(reverse('register_customer'),
                                    {'email': 'first@user.com', 'password': 'anyFirstPassword',
                                     'first_name': 'anyFirstName',
                                     'last_name': 'anyLastName'})
        self.assertEqual(response.data['status_code'], status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginCustomerTest(TestCase):
    def setUp(self):
        hashed_password = HashStringGenerator.generate('anyFirstPassword')
        Customer.objects.create(
            email='first@user.com', password=hashed_password, first_name='anyFirstName', last_name='anyLastName')

    def should_login_customer(self):
        # get API response
        response = self.client.post(reverse('login_customer'),
                                    {'email': 'first@user.com', 'password': 'anyFirstPassword'})
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)

    def should_return_error_when_login_customer_if_user_was_not_registered(self):
        # get API response
        response = self.client.post(reverse('login_customer'),
                                    {'email': 'first@user.com', 'password': 'anyPassword'})
        self.assertEqual(response.data['status_code'], status.HTTP_401_UNAUTHORIZED)


class RetrieveCustomerTest(TestCase):

    def setUp(self):
        self.first_customer = Customer.objects.create(
            email='first@user.com', password='anyFirstPassword', first_name='anyFirstName', last_name='anyLastName')
        self.second_customer = Customer.objects.create(
            email='second@user.com', password='anySecondPassword', first_name='secondFirstName',
            last_name='secondLastName')
        self.third_customer = Customer.objects.create(
            email='third@user.com', password='anyThirdPassword', first_name='thirdFirstName', last_name='thirdLastName')
        self.fourth_customer = Customer.objects.create(
            email='fourth@user.com', password='anyFourthPassword', first_name='fourthFirstName',
            last_name='fourthLastName')

    def should_retrieve_customer(self):
        response = client.get(
            reverse('get_delete_update_customer', kwargs={'pk': self.third_customer.pk}))
        customer = Customer.objects.get(pk=self.third_customer.pk)
        serializer = CustomerSerializer(customer)
        self.assertEqual(response.data['body'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def should_return_error_when_retrieve_customer_if_customer_does_not_exist(self):
        response = client.get(
            reverse('get_delete_update_customer', kwargs={'pk': 30}))
        self.assertEqual(response.data['status_code'], status.HTTP_404_NOT_FOUND)


class UpdateCustomerTest(TestCase):

    def setUp(self):
        self.first_customer = Customer.objects.create(
            email='first@user.com', password='anyFirstPassword', first_name='anyFirstName', last_name='anyLastName')
        self.second_customer = Customer.objects.create(
            email='second@user.com', password='anySecondPassword', first_name='secondFirstName',
            last_name='secondLastName')
        self.valid_payload = {
            'email': 'jackblack@gmail.com',
            'first_name': 'Jack',
            'last_name': 'Black'
        }
        self.invalid_payload = {
            'email': '',
            'first_name': 'Mehmet',
            'last_name': 'Yılmaz'
        }

    def should_update_customer(self):
        response = client.patch(
            reverse('get_delete_update_customer', kwargs={'pk': self.first_customer.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)

    def should_return_error_when_update_customer_if_payload_is_invalid(self):
        response = client.patch(
            reverse('get_delete_update_customer', kwargs={'pk': self.first_customer.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteCustomerTest(TestCase):

    def setUp(self):
        self.first_customer = Customer.objects.create(
            email='first@user.com', password='anyFirstPassword', first_name='anyFirstName', last_name='anyLastName')
        self.second_customer = Customer.objects.create(
            email='second@user.com', password='anySecondPassword', first_name='secondFirstName',
            last_name='secondLastName')

    def should_delete_customer(self):
        response = client.delete(
            reverse('get_delete_update_customer', kwargs={'pk': self.first_customer.pk}))
        self.assertEqual(response.data['status_code'], status.HTTP_204_NO_CONTENT)

    def should_return_error_when_delete_customer_if_customer_does_not_exist(self):
        response = client.delete(
            reverse('get_delete_update_customer', kwargs={'pk': 30}))
        self.assertEqual(response.data['status_code'], status.HTTP_404_NOT_FOUND)
