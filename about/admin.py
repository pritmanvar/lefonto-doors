from django.contrib import admin
from .models import WhyUsAbout, Expertise, About

@admin.register(WhyUsAbout)
class WhyUsAboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    list_filter = ['title']

@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'contact_number', 'website']
    search_fields = ['title', 'title_description', 'description', 'email', 'contact_number']
    filter_horizontal = ['why_us', 'expertise']
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'title_description', 'background_image', 'description']
        }),
        ('Why Us Section', {
            'fields': ['why_us_description', 'why_us_image', 'why_us']
        }),
        ('Additional Information', {
            'fields': ['image_2', 'question', 'answer', 'expertise']
        }),
        ('Contact Information', {
            'fields': ['contact_number', 'email', 'address', 'website']
        }),
    ]
