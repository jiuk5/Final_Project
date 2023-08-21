from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

        
class Profile(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return '%s.%s(%d)' % (self.title)
    