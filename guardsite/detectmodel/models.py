from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_image_extension(value):
    valid_extensions = ['.jpg', '.jpeg']
    extension = str(value).split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError('올바른 이미지 파일 형식이 아닙니다. (jpg, jpeg만 허용됩니다.)')

class DangerModel(models.Model):
    image = models.ImageField(upload_to='media/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])])
    danger = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-pk',)
        db_table = 'danger'
        
