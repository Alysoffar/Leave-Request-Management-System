from django.db import models # type: ignore
from django.urls import reverse # type: ignore
from django.utils import timezone 
from django.db.models.signals import post_save # type: ignore
from django.dispatch import receiver # type: ignore
from django.contrib.auth.models import AbstractUser
from user.models import Employee
from rest_framework.response import Response 
from rest_framework import status

# Create your models here.
STATUS_CHOICES=[
    ("Pending","Pending"),
    ("Accepted","Accepted"),
    ("Rejected","Rejected"),
]


class LeaveRequest(models.Model): # LeaveRequest
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    employee_id = models.ForeignKey(Employee , on_delete=models.CASCADE)
    #is_accepted = models.BooleanField(default=True) #nullable
    reason=models.TextField(max_length=2000,null=True,)
    status = models.CharField(max_length=200,
                              null=True,
                              choices=STATUS_CHOICES,
                              default="Pending") # must have choices


    def validate_date(self,start_date,end_date):
        if end_date < start_date: # =<
            return Response(status=status.HTTP_400_BAD_REQUEST)
        