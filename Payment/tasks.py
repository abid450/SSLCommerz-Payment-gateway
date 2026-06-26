# Payment/tasks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_payment_confirmation_email(self, transaction_id):
    """
    Send payment confirmation email to customer
    """
    try:
        from .models import PaymentTransaction
        
        # Get transaction from database
        transaction = PaymentTransaction.objects.get(id=transaction_id)
        
        # Prepare email context
        context = {
            'transaction': transaction,
            'tran_id': transaction.tran_id,
            'amount': transaction.amount,
            'payment_method': transaction.payment_method or 'N/A',
            'paid_at': transaction.paid_at or timezone.now(),
            'customer_name': transaction.customer_name,
            'customer_email': transaction.customer_email,
            'customer_phone': transaction.customer_phone,
            'customer_address': transaction.customer_address or 'N/A',
            'customer_city': transaction.customer_city or 'N/A',
            'year': timezone.now().year
        }
        
        # Render HTML email template
        html_content = render_to_string('payment_confirmation.html', context)
        text_content = strip_tags(html_content)
        
        subject = f'Payment Confirmation - {transaction.tran_id}'
        
        # Create email with HTML and plain text versions
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[transaction.customer_email],
            
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send()
        
        logger.info(f"Payment confirmation email sent to {transaction.customer_email}")
        return {'status': 'success', 'email': transaction.customer_email}
        
    except Exception as e:
        logger.error(f"Failed to send payment confirmation email: {str(e)}")
        raise self.retry(exc=e, countdown=60)
    


@shared_task
def send_pending_reminder():
    """
    Send reminder for pending transactions (optional)
    """
    from .models import PaymentTransaction
    
    pending_transactions = PaymentTransaction.objects.filter(
        status='pending',
        created_at__gte=timezone.now() - timedelta(hours=24)
    )
    
    sent_count = 1
    for transaction in pending_transactions:
        # Send reminder email
        subject = f'Payment Reminder - {transaction.tran_id}'
        message = f"""
        Dear {transaction.customer_name},
        
        Your payment with Transaction ID: {transaction.tran_id} is still pending.
        Amount: ৳{transaction.amount}
        Date: {transaction.created_at}
        
        If you have already made the payment, please ignore this message.
        
        Thank you,
        Your Team
        """
        
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [transaction.customer_email])
        sent_count += 1
    
    return {'status': 'success', 'sent_count': sent_count}


@shared_task
def cleanup_expired_transactions():
    """
    Clean up old pending/failed transactions
    """
    from .models import PaymentTransaction
    
    cutoff_date = timezone.now() - timedelta(days=7)
    
    # Delete or mark as expired
    expired_transactions = PaymentTransaction.objects.filter(
        status__in=['pending', 'initiated'],
        created_at__lte=cutoff_date
    )
    
    count = expired_transactions.count()
    expired_transactions.update(status='failed')
    
    logger.info(f"Cleaned up {count} expired transactions")
    return {'status': 'success', 'cleaned_up': count}