from django.db import models

# Create your models here.

class PhotoShare(models.Model):
    current_id = models.IntegerField()
    
    def __int__(self):
        return self.current_id

class Photo(models.Model):
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()
    
    def __str__(self):
        return self.description