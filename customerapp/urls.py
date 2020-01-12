from django.urls import path
from customer_api import views

urlpatterns = [
    path('api/v1/customers', views.CustomerList.as_view(), name='list_customers'),
    path('api/v1/customers/register', views.CustomerRegister.as_view(), name='register_customer'),
    path('api/v1/customers/login', views.CustomerLogin.as_view(), name='login_customer'),
    path('api/v1/customers/<int:pk>', views.CustomerDetail.as_view(), name='get_delete_update_customer')
]
