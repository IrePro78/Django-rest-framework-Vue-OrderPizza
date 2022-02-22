from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order import views
from order.views import CheckoutViewSet, OrdersListViewSet

router = DefaultRouter()

router.register("checkout", CheckoutViewSet, basename="order")
router.register("orders", OrdersListViewSet, basename="order")

urlpatterns = [
    path('', include(router.urls)),

]