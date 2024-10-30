from rest_framework import viewsets
from rest_framework.decorators import action 
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from store.tasks import send_bulk_email, send_low_stock_alert, send_order_confirmation
from .models import Category, Product, Cart, Order
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    CartSerializer, 
    OrderSerializer,
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Retrieve query parameters
        name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')
        is_trending = self.request.query_params.get('is_trending')

        # Apply filters based on query parameters
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)
        if is_trending is not None:
            queryset = queryset.filter(is_trending=is_trending.lower() in ['true', '1'])
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def alert_low_stock(self, request, pk=None):
        """Trigger low stock alert for a product"""
        send_low_stock_alert.delay(pk)
        return Response(
            {"message": "Low stock alert triggered"}, 
            status=status.HTTP_200_OK
        )


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Check if product already in cart
        product_id = request.data.get('product')
        existing_item = Cart.objects.filter(
            user=request.user,
            product_id=product_id
        ).first()

        if existing_item:
            # Update quantity instead of creating new item
            quantity = int(request.data.get('quantity', 1))
            existing_item.quantity += quantity
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data)

        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get('product', None)
        
        if product_id is not None:
            # Try to get single cart item for the specific product
            cart_item = Cart.objects.filter(
                user=request.user,
                product_id=product_id
            ).first()
            
            if not cart_item:
                return Response(
                    {"detail": "No cart item found for the specified product"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Serialize and return single item
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data)
        
        # If no product_id, return all cart items as before
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.prefetch_related('items').all()
        return Order.objects.prefetch_related('items').filter(user=user)

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        # Send order confirmation email asynchronously
        send_order_confirmation.delay(order.id)


class EmailViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def create(self, request):
        """Send bulk email to all users"""
        subject = request.data.get('subject')
        message = request.data.get('message')
        
        if not subject or not message:
            return Response(
                {"error": "Both subject and message are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Trigger async task
        send_bulk_email.delay(subject, message)
        
        return Response(
            {"message": "Bulk email sending initiated"}, 
            status=status.HTTP_202_ACCEPTED
        )