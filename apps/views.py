from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from apps.serializers import StudentSerializer
from authentication.models import Student


@extend_schema(tags=['student'], request=StudentSerializer)
class StudentFilterListView(ListAPIView):
    serializer_class = StudentSerializer
    def get_queryset(self):
        id = self.kwargs.get('pk')
        return Student.objects.filter(id=id)
