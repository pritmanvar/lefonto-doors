from django.contrib import admin
from .models import ContactQueries

@admin.register(ContactQueries)
class ContactQueriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']  # Show newest queries first
    
    fieldsets = [
        ('Contact Information', {
            'fields': ['name', 'email']
        }),
        ('Query Details', {
            'fields': ['message']
        }),
        ('Timestamp', {
            'fields': ['created_at']
        }),
    ]
