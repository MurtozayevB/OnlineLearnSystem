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

class Device(Model):
    device_id = CharField(max_length=255)
    student = ForeignKey('authentication.Student', on_delete=CASCADE, related_name='devices')
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.student.first_name


class Lesson(Model):
    title = CharField(max_length=255)
    description = TextField()
    video = FileField(upload_to='media/videos/lessons/lesson_videos')
    code = CharField(max_length=255)
    quote = CharField(max_length=255)
    image = ImageField(upload_to='media/images/lessons/lesson_images')
    thumbnail_image = ImageField(upload_to='media/images/lessons/thumbnail_images')


class Task(Model):
    class TypeChoices(TextChoices):
        easy = 'easy', "EASY"
        medium = 'medium', "MEDIUM"
        hard = 'hard', "HARD"

    title = CharField(max_length=255)
    description = TextField(blank=True)
    type = CharField(max_length=255, default=TypeChoices.medium)
    point = SmallIntegerField(default=1)
    lesson = ForeignKey('apps.Lesson', on_delete=CASCADE, related_name='tasks')


class History(Model):
    is_correct = BooleanField(default=False)
    created_at = DateTimeField(auto_created=True)
    task = ForeignKey('apps.Task', on_delete=CASCADE, related_name='history')
    student = ForeignKey('authentication.Student', on_delete=SET_NULL,null=True, related_name='history')

class Choice(Model):
    choice = CharField(max_length=255)
    task=ForeignKey(Task, on_delete=CASCADE, related_name='choices')
    is_correct = BooleanField(default=False)
    created_at = DateTimeField(auto_created=True)
    def __str__(self):
        return self.choice

class StudentDaily(Model):
    student = ForeignKey('authentication.Student', on_delete=CASCADE, related_name='daily_student')
    task = ForeignKey(Task, on_delete=CASCADE, related_name='daily_task')
    completed_at = DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.student.first_name

class DailyTask(Model):
    title = CharField(max_length=255)
    description = TextField()
    coin=SmallIntegerField(default=1)

    def __str__(self):
        return self.title

