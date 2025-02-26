from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from authentication.models import Student


class StatusSerializer(Serializer):
    status = CharField(max_length=120)


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = 'first_name', 'last_name', 'image', 'password', 'phone_number'

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'].method == 'POST':
            fields['image'].write_only = True
            fields['image'].required = False
            fields['password'].write_only = True
        if self.context['request'].method == 'GET':
            fields['first_name'].read_only = True
            fields['last_name'].read_only = True
            fields['phone_number'].read_only = True
        return fields

    def validate_password(self, value):
        return make_password(value)

    def validate_phone_number(self, value: str):
        if not (len(value) == 9 and value.isdigit()):
            raise ValidationError('Phone number is still wrong format')
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = StatusSerializer({'status': 200}).data
        return data