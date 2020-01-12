from rest_framework import routers
from customer_api import views as customerappviews

router = routers.DefaultRouter()
router.register(r'customers/register', customerappviews.CustomerRegister)
router.register(r'customers', customerappviews.CustomerList)
router.register(r'<int:pk>', customerappviews.CustomerDetail)