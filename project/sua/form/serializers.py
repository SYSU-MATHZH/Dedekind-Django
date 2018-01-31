from django.contrib.auth.models import User, Group
from project.sua.models import Student, SuaGroup, Sua, Application, Activity, Publicity, Appeal, Proof

from rest_framework import serializers

from django.contrib.auth.hashers import make_password


class AddUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, default='12345678')

    class Meta:
        model = User
        fields = ('password', )


class AddStudentSerializer(serializers.ModelSerializer):
    user = AddUserSerializer()

    class Meta:
        model = Student
        fields = ('id', 'number', 'name', 'suahours', 'grade', 'classtype', 'phone', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(
            username=validated_data['number'],
            password=make_password(user_data['password']),
        )
        student = Student.objects.create(user=user, **validated_data)
        return student
