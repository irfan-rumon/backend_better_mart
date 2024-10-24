from celery import shared_task
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from account.models import User
from .models import Order, Product

@shared_task
def send_low_stock_alert(product_id):
    """Send alert when product stock is low"""
    try:
        product = Product.objects.get(id=product_id)
        admin_users = User.objects.filter(is_staff=True)
        
        subject = f'Low Stock Alert - {product.name}'
        message = f'The stock for {product.name} is running low. Current quantity: {product.quantity}'
        
        for admin in admin_users:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[admin.email],
                fail_silently=False,
            )
        
        return f"Low stock alert sent for {product.name}"
    except Product.DoesNotExist:
        return "Product not found"

@shared_task
def send_bulk_email(subject, message):
    """Send email to all users"""
    try:
        # Get all active users' email addresses
        user_emails = User.objects.filter(is_active=True).values_list('email', flat=True)
        
        # Create mass email data
        messages = [(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        ) for email in user_emails]
        
        # Send mass mail
        send_mass_mail(messages, fail_silently=False)
        
        return f"Bulk email sent to {len(user_emails)} users"
    except Exception as e:
        return f"Error sending bulk email: {str(e)}"

@shared_task
def send_order_confirmation(order_id):
    """Send order confirmation email"""
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order Confirmation - Order #{order.id}'
        message = f"""
        Dear {order.user.email},

        Thank you for your order! Here are your order details:

        Order ID: {order.id}
        Total Amount: ${order.total_amount}
        Status: {order.status}

        Order Items:
        """
        
        for item in order.items.all():
            message += f"\n- {item.product.name} x {item.quantity} @ ${item.price} each"
        
        message += "\n\nThank you for shopping with us!"
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        
        return f"Order confirmation sent for Order #{order.id}"
    except Order.DoesNotExist:
        return "Order not found"