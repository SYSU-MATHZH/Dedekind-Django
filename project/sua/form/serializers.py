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


class AddSuaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sua
        fields = ('id', 'activity', 'student', 'team', 'suahours')


class AddActivitySerializer(serializers.ModelSerializer):
    suas = AddSuaSerializer(many=True)

    class Meta:
        model = Activity
        fields = ('id', 'title', 'detail', 'group', 'date', 'suas')

    def create(self, validated_data):
        sua_datas = validated_data.pop('suas')
        activity = Activity.objects.create(**validated_data)
        owner = validated_data['owner']
        for sua_data in sua_datas:
            sua = Sua.objects.create(owner=owner, activity=activity, **sua_data)
        return activity


class AddAppealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appeal
        fields = ('id','student', 'publicity', 'content', 'status', 'is_checked', 'feedback')

#    def create(self,validated_data):
#        appeal = Appeal.objects.create(**validated_data)
#        return appeal

class AddPublicitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicity
        fields = ('id', 'owner', 'activity', 'title', 'content', 'contact', 'is_published', 'begin', 'end')

class AddProofSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proof
        fields = ('id', 'is_offline', 'proof_file')

    def create(self, validated_data):
        if validated_data['is_offline']:
            proof = Proof.objects.create(**validated_data)
            return proof
        else:
            if validated_data.get('proof_file',None):
                proof = Proof.objects.create(**validated_data)
                return proof
            else:
                messagebox.showwarning('提示', '请上传线上文件')
