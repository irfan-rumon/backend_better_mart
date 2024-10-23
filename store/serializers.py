from rest_framework import serializers
from .models import Category, Product, Cart, Order  

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'price', 'image_link', 'created_at']

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_name', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['user']

class OrderSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField()),
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'product_ids', 'total_amount', 'status', 'created_at']
        read_only_fields = ['user', 'created_at', 'total_amount']  # Make total_amount read-only

    def create(self, validated_data):
        product_ids = validated_data.pop('product_ids', None)

        if not product_ids:
            raise serializers.ValidationError("No products provided for the order")

        # Calculate total amount
        total_amount = sum(
            Product.objects.get(id=product_id['id']).price * product_id['quantity'] 
            for product_id in product_ids
        )

        # Create the order with the calculated total_amount
        order = Order.objects.create(
            user=validated_data['user'],
            total_amount=total_amount,
            status='pending',
            product_ids=product_ids  # Save the product_ids in the JSON field
        )

        return order