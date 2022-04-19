from django.contrib import admin

from cart.models import Cart, OrderItem

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'step', )
    list_filter = ('created', )
    inlines = [OrderItemInline,]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'course', )
    list_filter = ('created', )
