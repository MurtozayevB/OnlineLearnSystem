from django.utils.timezone import localtime
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from apps.models import Lesson, StudentDaily, History
from authentication.models import Student


class LessonSerializer(ModelSerializer):
    progress = SerializerMethodField()
    class Meta:
        model = Lesson
        fields = ['id', 'title','progress']


    def get_progress(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 0

        student = request.user

        total_tasks = obj.tasks.count()
        correct_tasks = obj.tasks.filter(
            history__student=student, history__is_correct=True
        ).distinct().count()

        return round((correct_tasks / total_tasks) * 100, 2) if total_tasks else 0

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['progress'] = self.get_progress(instance)
        return data





class StudentSerializer(ModelSerializer):
    rank = SerializerMethodField()
    last_theme = LessonSerializer()
    streak = SerializerMethodField()

    class Meta:
        model = Student
        fields = ['pk','first_name', 'last_name', 'phone_number', 'image', 'streak', 'point', 'rank', 'last_theme', 'coin']



    def get_rank(self, obj):
        higher_rank_count = Student.objects.filter(point__gt=obj.point).count()
        return higher_rank_count + 1

    def get_streak(self, obj):
        tasks = (
            StudentDaily.objects.filter(student=obj)
            .order_by('-completed_at')
            .values_list('completed_at', flat=True)
        )

        if not tasks or tasks[0] is None:
            return 0

        streak = 1
        prev_date = localtime(tasks[0]).date()

        for date in tasks[1:]:
            if date is None:
                continue
            date = localtime(date).date()
            if (prev_date - date).days == 1:
                streak += 1
            elif (prev_date - date).days > 1:
                break
            prev_date = date

        return streak

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['streak'] = self.get_streak(instance)
        return data