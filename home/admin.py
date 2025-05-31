from django.contrib import admin
from .models import Banner, Home

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['description', 'product_material']
    list_filter = ['product_material']
    search_fields = ['description']

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'question']
    search_fields = ['title', 'description', 'question', 'answer']
    filter_horizontal = ['categories', 'features']
    