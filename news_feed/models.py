from django.db import models
from django.contrib.auth.models import User

class SourceCategory(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    adding_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adding_date']
        unique_together = ['title', 'user']  # Ensure unique titles per user

    def __str__(self):
        return self.title


class NewsSource(models.Model):
    title = models.CharField(max_length=255, default='Untitled')
    url = models.URLField()
    category = models.ForeignKey(SourceCategory, on_delete=models.CASCADE, null=True)
    adding_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adding_date']

    def __str__(self):
        return self.url
