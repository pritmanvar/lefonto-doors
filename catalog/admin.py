from django.contrib import admin
from .models import WhyUsCatalog, Catalog

@admin.register(WhyUsCatalog)
class WhyUsCatalogAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    list_filter = ['title']
    
    readonly_fields = ('image_tag',)

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'description']
    search_fields = ['about', 'description']
    # filter_horizontal = ['why_us']
    
    readonly_fields = ('image_tag',)
