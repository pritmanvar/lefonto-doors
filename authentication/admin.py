from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Location
from django.utils.html import format_html
import json

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'role', 'address_city', 'address_country', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'role', 'address_country', 'address_state', 'address_city')
    search_fields = ('email', 'name', 'address_country', 'address_state', 'address_city', 'address_landmark')
    ordering = ('email',)
    
    fieldsets = (
        ('Authentication', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role')}),
        ('Address Information', {
            'fields': (
                'address_country', 'address_state', 'address_city',
                'address_house_no', 'address_landmark', 'address_pincode'
            ),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'role', 'password1', 'password2',
                'address_country', 'address_state', 'address_city',
                'address_house_no', 'address_landmark', 'address_pincode',
                'is_staff', 'is_active'
            )}
        ),
    )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'state', 'city', 'pincode', 'landmark', 'updated_by', 'created_at')
    list_filter = ('country', 'state', 'city', 'updated_by')
    search_fields = ('country', 'state', 'city', 'pincode', 'landmark')
    readonly_fields = ('created_at', 'updated_at', 'updated_by')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Location Information', {
            'fields': ('country', 'state', 'city', 'pincode', 'landmark')
        }),
        ('Metadata', {
            'fields': ('updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
