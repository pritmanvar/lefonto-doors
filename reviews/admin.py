from django.contrib import admin

@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['user__email', 'product__product_name', 'review_text']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user', 'product']
    
    fieldsets = [
        ('Review Information', {
            'fields': ['user', 'product', 'rating']
        }),
        ('Review Content', {
            'fields': ['review_text']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def get_ordering(self, request):
        return ['-created_at']  # Show newest reviews first
