from django.urls import path

from order import views

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view()),
    path('orders/', views.OrdersList.as_view()),
]