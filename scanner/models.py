from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    role = models.CharField(max_length=50,default='student')
    roll_number = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    qr = models.ImageField(upload_to='qr/',blank=True)
    def __str__(self):
        return f'{self.username}+{self.id}'

class Report(models.Model):
    roll_number = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.id}'

class Attendance(models.Model):
    roll_number = models.CharField(max_length=50)
    present = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.id}'
