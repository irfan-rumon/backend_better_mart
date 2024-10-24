from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    EmailViewSet,
    ProductViewSet,
    CartViewSet,
    OrderViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'emails', EmailViewSet, basename='email')


urlpatterns = [
    path('', include(router.urls)),
]