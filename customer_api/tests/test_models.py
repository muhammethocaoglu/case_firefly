from django.test import TestCase
from ..models import Customer


class CustomerTest(TestCase):
    def setUp(self):
        Customer.objects.create(
            email='mail@mail.com', password='anyPassword', first_name='anyFirstName', last_name='anyLastName')

    def should_create_customer(self):
        any_customer = Customer.objects.get(email='mail@mail.com')
        self.assertEqual(any_customer.first_name, "anyFirstName")
        self.assertEqual(any_customer.last_name, "anyLastName")
        self.assertEqual(any_customer.password, "anyPassword")
