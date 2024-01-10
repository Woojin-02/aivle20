from django.db import models
from django.conf import settings

class DangerModel(models.Model):
    image = models.ImageField(upload_to='media/')
    danger = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-pk',)
        db_table = 'danger'
        
