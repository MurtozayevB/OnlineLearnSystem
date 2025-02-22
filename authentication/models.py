import datetime
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, CharField, ImageField, SlugField, ForeignKey, DecimalField, SET_NULL, CASCADE, \
    DateTimeField, ManyToManyField, SmallIntegerField, TextField, UUIDField, BooleanField, TextChoices, IntegerField, \
    FileField
from django.utils.text import slugify


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


class Student(AbstractUser):
    phone_number = CharField(max_length=20, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    username = None

    #     custom fields
    image = ImageField(null=True, blank=True, upload_to='media/images/student/avatar')
    strike = CharField(null=True, blank=True, max_length=255)
    point = SmallIntegerField(null=True, blank=True)
    last_theme=ForeignKey('apps.Lesson',on_delete=SET_NULL, null=True, blank=True)
    coin = IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'




