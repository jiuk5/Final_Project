from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return f'uploads/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    # imgfile = models.ImageField(null=True, upload_to="", blank=True)
    imgfile = models.FileField(null=True, upload_to= user_directory_path, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)