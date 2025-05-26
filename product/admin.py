from django.contrib import admin
from .models import (
    Category, ProductMaterial, Style, Color, Size, Feature,
    Product, ProductSize, ProductImage
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ['material_name']
    search_fields = ['material_name']

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ['style_name']
    search_fields = ['style_name']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'color_code']
    search_fields = ['color_name', 'color_code']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['height', 'width', '__str__']
    search_fields = ['height', 'width']

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['feature_name']
    search_fields = ['feature_name']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'material', 'style', 'ratings', 'created_at']
    list_filter = ['category', 'material', 'style', 'created_at']
    search_fields = ['product_name', 'details', 'short_description']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['color', 'features', 'recommanded_products']
    inlines = [ProductSizeInline, ProductImageInline]
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['product_name', 'short_description', 'details', 'main_image']
        }),
        ('Classifications', {
            'fields': ['category', 'material', 'style']
        }),
        ('Specifications', {
            'fields': ['thickness', 'weight', 'color']
        }),
        ('Features & Recommendations', {
            'fields': ['features', 'recommanded_products']
        }),
        ('Customer Information', {
            'fields': ['warranty_details', 'return_policy', 'ratings']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'price', 'discount']
    list_filter = ['product', 'size']
    search_fields = ['product__product_name']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product']
    list_filter = ['product']
    search_fields = ['product__product_name']
