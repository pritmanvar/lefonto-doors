from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_active', 'city', 'country')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_google_login', 'country', 'state', 'city')
    search_fields = ('email', 'name', 'country', 'state', 'city')
    ordering = ('email',)
    
    fieldsets = (
        ('Authentication', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Address Information', {
            'fields': (
                'country', 'state', 'city', 'sub_district', 
                'street_name', 'pincode', 'address'
            ),
        }),
        ('Login Info', {'fields': ('is_google_login',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'password1', 'password2', 'is_staff',
                'is_active', 'country', 'state', 'city'
            )}
        ),
    )
