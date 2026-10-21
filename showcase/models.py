from django.db import models
from django.utils.html import mark_safe

class ImageShowcase(models.Model):
    """
    A model that stores and displays images with titles, descriptions,
    categories, and automatic thumbnail rendering.
    """
    CATEGORY_CHOICES = [
        ('Technology', 'Technology & Architecture'),
        ('Nature', 'Nature & Landscapes'),
        ('Design', 'Digital Art & UI/UX'),
        ('Abstract', 'Abstract & Creative'),
    ]

    title = models.CharField(
        max_length=150,
        help_text="Enter a title or caption for the image."
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description or context for this image."
    )
    image = models.ImageField(
        upload_to='gallery/',
        help_text="Upload an image file (PNG, JPG, WebP, GIF)."
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Accessibility alt text describing the image content."
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Technology',
        help_text="Categorize this image showcase."
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Highlight this image prominently at the top of the gallery."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the image was uploaded."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Image Showcase"
        verbose_name_plural = "Image Showcases"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-fill alt_text from title if left blank
        if not self.alt_text:
            self.alt_text = f"Showcase image for {self.title}"
        super().save(*args, **kwargs)

    @property
    def file_size_display(self):
        """Returns human-readable file size."""
        try:
            if self.image and hasattr(self.image, 'size'):
                size = self.image.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                else:
                    return f"{size / (1024 * 1024):.2f} MB"
        except Exception:
            pass
        return "Unknown"

    def image_preview(self):
        """Displays thumbnail preview in Django Admin."""
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" '
                f'style="max-width: 120px; max-height: 90px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd; box-shadow: 0 2px 8px rgba(0,0,0,0.15);" />'
            )
        return "No Image"

    image_preview.short_description = "Thumbnail Preview"
