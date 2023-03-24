
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user=models.IntegerField()
    cv=models.FileField(upload_to='images')
    
    

class CheckResume(models.Model):
    user=models.IntegerField()
    statut=models.CharField(max_length=50)
    score=models.FloatField()
    
    def __str__(self):
        return self.statut

                        
    
    
    