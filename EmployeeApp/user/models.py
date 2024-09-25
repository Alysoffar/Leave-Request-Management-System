from django.db import models # type: ignore
from django.urls import reverse # type: ignore
from django.utils import timezone # type: ignore
from PIL import Image # type: ignore
from django.db.models.signals import post_save # type: ignore
from django.dispatch import receiver # type: ignore
from django.contrib.auth.models import BaseUserManager, AbstractUser

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self,username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Employee(AbstractUser):
    leave_balance = models.IntegerField(default=50,null=True,blank=True)
    manager= models.ForeignKey("Employee",on_delete=models.CASCADE,null=True, blank=True) #manger
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=20)
    image=models.ImageField(default='default.jpg', null=True , blank=True)

    objects=MyUserManager()

    def __str__(self):
        return self.username
    
