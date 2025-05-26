from django.contrib import admin
from .models import Banner, Home

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['description', 'product_material', 'is_active']
    list_filter = ['is_active', 'product_material']
    search_fields = ['description']
    raw_id_fields = ['product_material']
    
    fieldsets = [
        ('Banner Content', {
            'fields': ['description', 'image']
        }),
        ('Product Association', {
            'fields': ['product_material']
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'question']
    search_fields = ['title', 'description', 'question', 'answer']
    filter_horizontal = ['categories', 'features']
    
    fieldsets = [
        ('Main Content', {
            'fields': ['title', 'description', 'background_image']
        }),
        ('Categories Section', {
            'fields': ['categories']
        }),
        ('Q&A Section', {
            'fields': ['question', 'answer']
        }),
        ('Features Section', {
            'fields': ['features']
        }),
    ]
