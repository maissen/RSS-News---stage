from django.db import models


class NewsSource(models.Model):
    link = models.URLField(unique=True)
    adding_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adding_date']

    def __str__(self):
        return self.link