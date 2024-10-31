from rest_framework import serializers
from .models import Category, Product, Cart, Order, OrderItem
from django.db import transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'image_link']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'price', 'image_link', 'created_at', 'is_trending']

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    image_link = serializers.CharField(source='product.image_link', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_name', 'quantity', 'total_price', 'created_at', 'image_link']
        read_only_fields = ['user']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_amount', 'status', 'created_at']
        read_only_fields = ['user', 'created_at', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_amount = 0

        with transaction.atomic():
            # First create the order
            order = Order.objects.create(
                user=validated_data['user'],
                total_amount=0,
                status='pending'
            )

            # Create order items
            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                price = product.price
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                
                total_amount += price * quantity

            # Update order total
            order.total_amount = total_amount
            order.save()

        return order