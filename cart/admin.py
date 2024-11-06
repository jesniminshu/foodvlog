from django.contrib import admin
from . models import *

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # number of empty forms to display

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'total_amount', 'date_ordered', 'completed')  # Customize as needed
    list_filter = ('completed', 'date_ordered')  # Add filters if needed

admin.site.register(Order, OrderAdmin)
admin.site.register(cartlist)
admin.site.register(items)