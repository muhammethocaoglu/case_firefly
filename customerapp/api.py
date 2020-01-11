from rest_framework import routers
from customer_api import views as customerappviews

router = routers.DefaultRouter()
router.register(r'customers', customerappviews.CustomerView)