from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.

class Notice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now=True)
    etc = models.CharField(max_length=20)
    

    class Meta:
        ordering = ('-pk',)
        db_table = 'notice'     
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("communities:detail", kwargs={"notice_pk":self.pk})
    
    
class Comment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pk',)
        db_table = 'comment' 

    def __str__(self):
        return self.content