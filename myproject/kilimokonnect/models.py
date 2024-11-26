from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator # type: ignore
from decimal import Decimal
from django.conf import settings # type: ignore
from django.utils import timezone # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager # type: ignore
from django.utils.translation import gettext_lazy as _ # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore


class CustomUser (BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser (AbstractUser ):
    USER_TYPE_CHOICES = (
        ('owner', 'Owner'),
        ('retailer', 'Retailer')
    )

    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default='retailer'
    )
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    username = None  # Remove username field since we're using email as USERNAME_FIELD
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    objects = CustomUser ()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User '
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

class FreshProduceRetailer(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    business_address = models.TextField()
    business_registration = models.CharField(max_length=50, unique=True)
    tax_number = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


class ProduceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    storage_requirements = models.TextField()
    shelf_life = models.IntegerField(help_text="Shelf life in days")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Produce Categories"

class FreshProduce(models.Model):
    QUALITY_GRADES = [
        ('A', 'Premium Grade'),
        ('B', 'Standard Grade'),
        ('C', 'Economy Grade'),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProduceCategory, on_delete=models.CASCADE)
    quality_grade = models.CharField(max_length=1, choices=QUALITY_GRADES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    harvest_date = models.DateField()
    expiry_date = models.DateField()
    is_organic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Grade {self.quality_grade}"

    def is_expired(self):
        return self.expiry_date < timezone.now().date()

class Order(models.Model):
    ORDER_STATUS = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    retailer = models.ForeignKey(FreshProduceRetailer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address = models.TextField()
    order_notes = models.TextField(blank=True)
    order_reference = models.CharField(max_length=50, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_reference:
            import uuid
            self.order_reference = f"ORD-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_reference} - {self.retailer.business_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    produce = models.ForeignKey(FreshProduce, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produce.name} - {self.quantity}"

class QualityCheck(models.Model):
    RESULT_CHOICES = [
        ('PASS', 'Passed'),
        ('FAIL', 'Failed'),
        ('PENDING', 'Pending Review'),
    ]

    produce = models.ForeignKey(FreshProduce, on_delete=models.CASCADE)
    inspection_date = models.DateTimeField(auto_now_add=True)
    inspector_name = models.CharField(max_length=255)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    visual_inspection = models.TextField()
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Quality Check - {self.produce.name} - {self.inspection_date}"

class RetailerReview(models.Model):
    retailer = models.ForeignKey(FreshProduceRetailer, on_delete=models.CASCADE)


class StorageOwner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    registration_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name

    class Meta:
        ordering = ['-created_at']

class StorageFacility(models.Model):
    FACILITY_TYPES = [
        ('WAREHOUSE', 'Warehouse'),
        ('COLD_STORAGE', 'Cold Storage'),
        ('SILO', 'Silo'),
        ('GRAIN_STORE', 'Grain Store'),
    ]

    owner = models.ForeignKey(StorageOwner, on_delete=models.CASCADE, related_name='facilities')
    name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)  # in metric tons
    available_space = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    gps_coordinates = models.CharField(max_length=50, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # price per ton
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.facility_type}"

    class Meta:
        verbose_name_plural = "Storage Facilities"

class Product(models.Model):
    PRODUCT_CATEGORIES = [
        ('GRAINS', 'Grains'),
        ('FRUITS', 'Fruits'),
        ('VEGETABLES', 'Vegetables'),
        ('DAIRY', 'Dairy Products'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=PRODUCT_CATEGORIES)
    description = models.TextField()
    unit = models.CharField(max_length=50)  # e.g., kg, tons, boxes
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

class StorageBooking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    facility = models.ForeignKey(StorageFacility, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    booking_reference = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate unique booking reference
            import uuid
            self.booking_reference = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.facility.name}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    PAYMENT_METHODS = [
        ('MPESA', 'M-Pesa'),
        ('BANK', 'Bank Transfer'),
        ('CARD', 'Credit Card'),
    ]

    booking = models.ForeignKey(StorageBooking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    transaction_reference = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_reference} - {self.payment_status}"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    facility = models.ForeignKey(StorageFacility, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.facility.name}"