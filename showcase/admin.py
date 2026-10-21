from django.contrib import admin
from .models import ImageShowcase

@admin.register(ImageShowcase)
class ImageShowcaseAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'is_featured', 'file_size_display', 'created_at')
    list_display_links = ('title',)
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'alt_text')
    readonly_fields = ('image_preview', 'file_size_display', 'created_at')
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'category', 'image', 'image_preview', 'alt_text')
        }),
        ('Details & Meta', {
            'fields': ('description', 'is_featured', 'file_size_display', 'created_at')
        }),
    )
