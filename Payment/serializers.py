# apps/payment/serializers.py
from rest_framework import serializers
from .models import PaymentTransaction, PaymentLog

class PaymentInitiateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)
    currency = serializers.CharField(default='BDT', max_length=10)
    customer_name = serializers.CharField(max_length=100)
    customer_email = serializers.EmailField(
        required = True,
        error_messages={
            'required': 'Email address is required',
            'blank': 'Email cannot be empty',
            'invalid': 'Please enter a valid email address'
        }
    )
    customer_phone = serializers.CharField(max_length=20)
    customer_address = serializers.CharField(required=True, error_messages={

        'required': 'Email address is required',
        'blank': 'Address cannot be empty',
        'invalid': 'Please enter your Permanent address'
    })
    customer_city = serializers.CharField(max_length=50, required=True)
    order_id = serializers.CharField(required=False, allow_blank=True)
    product_name = serializers.CharField(default='Payment', max_length=200)
    product_category = serializers.CharField(default='General', max_length=100)
    num_of_item = serializers.IntegerField(default=1, min_value=1)
    
    def validate_customer_phone(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("Please enter your correct number.")     

        elif PaymentTransaction.objects.filter(customer_phone=value).exists():
            raise serializers.ValidationError('Phone number already used! Please try to another number. ')   
        
        return value
    
    def validate_amount(self, value):
        """Validate amount"""
        if value < 500:
            raise serializers.ValidationError("Amount must be greater than 500")
        
        if value > 1000000:  # 10 Lakh BDT
            raise serializers.ValidationError("Amount exceeds maximum limit (1,000,000 BDT)")
        
        return value
    

    def validate_customer_email(self, value):
        if PaymentTransaction.objects.filter(customer_email__iexact=value).exists():
            raise serializers.ValidationError('Email already taken! Please try to another email.')
        return value


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'
        read_only_fields = ['id', 'tran_id', 'sessionkey', 'val_id', 'created_at', 'updated_at', 'paid_at']


class PaymentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = '__all__'