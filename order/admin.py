from django.contrib import admin
from.models import Order,Order_Item

# Register your models here.
class OrderItemTubleInline(admin.TabularInline):
    model=Order_Item
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTubleInline,]
