from django import forms # type: ignore
from django.contrib import admin # type: ignore
from .models import (
    CustomUser,
    FreshProduceRetailer,
    ProduceCategory,
    FreshProduce,
    Order,
    OrderItem,
    QualityCheck,
    RetailerReview,
    StorageOwner,
    StorageFacility,
    Product,
    StorageBooking,
    Payment,
    Review
)

class FreshProduceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quality_grade', 'unit_price', 'available_quantity')
    search_fields = ('name', 'category__name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_reference', 'retailer', 'status', 'total_amount', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('order_reference', 'retailer__business_name')

#class CustomUser Admin(UserAdmin):
 #   model = CustomUser 


# Register the models
admin.site.register(CustomUser)
admin.site.register(FreshProduceRetailer)
admin.site.register(ProduceCategory)
admin.site.register(FreshProduce, FreshProduceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(QualityCheck)
admin.site.register(RetailerReview)
admin.site.register(StorageOwner)
admin.site.register(StorageFacility)
admin.site.register(Product)
admin.site.register(StorageBooking)
admin.site.register(Payment)
admin.site.register(Review)
