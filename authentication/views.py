from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from .models import Student
from .serializers import RegisterModelSerializer


@extend_schema(tags=['auth'], request=RegisterModelSerializer)
class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterModelSerializer(data=request.data, context={'request': request})
        user = Student.objects.filter(phone_number=request.data.get("phone_number")).first()

        if serializer.is_valid() or (user and not user.is_active):
            if not user:
                u = serializer.save()
                u.is_active = True
                u.save()

            return Response({
                "first_name": serializer.validated_data.get("first_name"),
                "last_name": serializer.validated_data.get("last_name"),
                "phone_number": serializer.validated_data.get("phone_number"),
            }, status=HTTP_201_CREATED)

        elif user and user.is_active:
            return Response({
                "status": 400,
                "message": "Telefon raqami oldin ro'yxatdan o'tgan!"
            }, status=HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
