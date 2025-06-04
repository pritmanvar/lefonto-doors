from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Location
from django.utils.html import format_html
import json

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('mobile', 'email', 'name', 'role', 'location', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'role', 'location')
    search_fields = ('email', 'name', 'location__name')
    ordering = ('email',)

    fieldsets = (
        ('Authentication', {'fields': ('mobile', 'password')}),
        ('Personal Info', {'fields': ('name', 'role', 'email', 'profile_image', 'image_tag')}),
        ('Address Information', {'fields': ('location',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined', 'created_at', 'updated_at', 'image_tag')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2', 'name', 'role', 'email', 'location', 'image_tag'),
        }),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'state', 'city', 'pincode', 'landmark', 'created_at')
    list_filter = ('country', 'state', 'city')
    search_fields = ('country', 'state', 'city', 'pincode', 'landmark')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
