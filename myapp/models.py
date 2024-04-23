from django.db import models

# Create your models here.
class users(models.Model):
    name=models.CharField(max_length=25)
    username=models.CharField(max_length=25)
    email=models.CharField(max_length=25)
    password=models.CharField(max_length=25)
    confirmpassword=models.CharField(max_length=25)  
    mobilenumber=models.IntegerField() 
class contact(models.Model):
    Name=models.CharField(max_length=25)
    Email=models.CharField(max_length=25)
    Message=models.TextField()