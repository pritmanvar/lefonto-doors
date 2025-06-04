from django.contrib import admin
from .models import WhyUsAbout, Expertise, About

@admin.register(WhyUsAbout)
class WhyUsAboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    list_filter = ['title']
    
    readonly_fields = ('image_tag',)

@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'contact_number', 'website']
    search_fields = ['title', 'title_description', 'description', 'email', 'contact_number']
    filter_horizontal = ['why_us', 'expertise']
    
    readonly_fields = (
        'background_image_tag',
        'why_about_us_image_tag',
        'image_2_tag'
    )