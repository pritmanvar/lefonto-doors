from django.contrib import admin
from .models import CustomerReview

@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['user__mobile', 'product__product_name', 'review_text']
    readonly_fields = ['created_at']
        
    def get_ordering(self, request):
        return ['-created_at']  # Show newest reviews first
