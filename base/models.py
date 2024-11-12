from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    path = models.CharField(max_length=255, blank=True, help_text="Direct URL path to the article's dedicated page")
    image_path = models.CharField(max_length=255, blank=True, help_text="URL or path to the article's image")  # Placeholder for image path
    group = models.CharField(max_length=100, blank=True, help_text="Category or group of the article, e.g., 'Statistics'")  # Placeholder for group
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Ensure `path` is absolute by adding a leading `/` if missing
        if self.path and not str(self.path).startswith('/'):
            return f"/{self.path}"
        return str(self.path) if self.path else "#"

    def __str__(self):
        return self.title
