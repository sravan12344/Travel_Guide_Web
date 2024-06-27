from django.db import models
from django.contrib.auth.models import User
class Register(models.Model):
    fullname = models.CharField(max_length=250)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=80)
    confirm_password = models.CharField(max_length=80)
    otp = models.IntegerField(null=True,blank=True)

    def _str_(self):
        return self.username

    def isExistsphone(self):
        if Register.objects.filter(mobile=self.mobile):
            return True

        return False

    def isExistsemail(self):
        if Register.objects.filter(email=self.email):
            return True

        return False

class contact(models.Model):
    name=models.CharField(max_length=100,null=True,blank=False,default=True)
    email=models.EmailField(max_length=30)
    subject=models.CharField(max_length=50,null=True,blank=False,default=True)
    message=models.TextField()
    def _str_(self):
        return self.name

class TourBooking(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, default=True)
    booking_date = models.DateField()


    def _str_(self):
        return self.name

class Ticket(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, default=True)
    ticket_no = models.PositiveIntegerField(null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    gender = models.BooleanField()

    def __str__(self):
        return f"Ticket No: {self.ticket_no} - {self.first_name} {self.last_name}"
    
