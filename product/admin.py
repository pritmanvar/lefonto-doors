from django import forms
from django.contrib import admin
from django_jsonform.models.fields import JSONField, ArrayField

from .models import (
    DoorCategory,
    DoorStyle,
    DoorDimension,
    DoorColor,
    DoorMaterial,
    Feature,
    GallarySupporting,
    Product,
)

@admin.register(DoorCategory)
class DoorCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'updated_by')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DoorStyle)
class DoorStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'updated_by')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DoorDimension)
class DoorDimensionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'thickness', 'height', 'width', 'created_at', 'updated_at', 'updated_by')
    list_filter = ('thickness_measure', 'height_measure', 'width_measure')
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DoorColor)
class DoorColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code', 'created_at', 'updated_at', 'updated_by')
    search_fields = ('name', 'color_code')
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DoorMaterial)
class DoorMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'updated_by')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name',)
    search_fields = ('feature_name',)

@admin.register(GallarySupporting)
class GallarySupportingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at', 'updated_at', 'updated_by')
    list_filter = ('product', 'user')
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

# class ProductForm(forms.ModelForm):
#     variants = JSONField()
#     colors = JSONField()
    
#     class Meta:
#         model = Product
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Set schemas dynamically
#         self.fields['variants'].schema = Product.get_variant_schema()
#         self.fields['colors'].schema = Product.get_color_schema()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # form = ProductForm
    list_display = ('product_name', 'category', 'style', 'ratings', 'created_at', 'updated_at', 'updated_by')
    list_filter = ('category', 'style', 'features')
    search_fields = ('product_name', 'details', 'short_description')
    filter_horizontal = ('features', 'recommanded_products')
    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
