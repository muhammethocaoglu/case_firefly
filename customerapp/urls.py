from django.urls import path
from customer_api import views

urlpatterns = [
    path('api/v1/customers/', views.CustomerList.as_view()),
    path('api/v1/customers/register/', views.CustomerRegister.as_view()),
    path('api/v1/customers/login/', views.CustomerLogin.as_view()),
    path('api/v1/customers/<int:pk>/', views.CustomerDetail.as_view())
]
