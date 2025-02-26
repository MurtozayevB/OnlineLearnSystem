from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.models import History  # History modelini chaqiramiz
from authentication.models import Student  # Student modelini chaqiramiz

@receiver(post_save, sender=History)
def update_student_point(sender, instance, created, **kwargs):
    if created and instance.is_correct and instance.student:
        student = instance.student
        student.point = (student.point or 0) + 1
        student.save()
