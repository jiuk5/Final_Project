from django.db import models

class Profile(models.Model):
    # imgfile = models.ImageField(null=True, upload_to="", blank=True)
    imgfile = models.FileField(null=True, upload_to="", blank=True)
    