from django.db import models

class AdminTools(models.Model):
    class Meta:
        verbose_name = "📊 Admin Dashboard"
        verbose_name_plural = "📊 Admin Dashboard"

    def __str__(self):
        return "Click the custom dashboard link in menu."