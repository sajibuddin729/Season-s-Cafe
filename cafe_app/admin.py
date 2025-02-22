from django.contrib import admin

# Register your models here.

from .models import Category, MenuItem, Reservation, Order, OrderItem, Feedback

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_special']
    list_filter = ['category', 'is_available', 'is_special']
    search_fields = ['name', 'description']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'time', 'guests', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['name', 'email', 'phone']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone']
    inlines = [OrderItemInline]

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['name', 'email', 'message']