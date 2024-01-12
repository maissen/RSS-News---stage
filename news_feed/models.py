from django.db import models

class SourceCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    adding_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adding_date']

    def __str__(self):
        return self.title


class NewsSource(models.Model):
    url = models.URLField(unique=True)
    category = models.ForeignKey(SourceCategory, on_delete=models.CASCADE, null=True)
    adding_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adding_date']

    def __str__(self):
        return self.url
