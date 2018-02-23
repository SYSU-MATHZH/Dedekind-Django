from django.contrib.auth.models import User, Group
from project.sua.models import Student, SuaGroup, Sua, Application, Activity, Publicity, Appeal, Proof

from rest_framework import serializers

from django.contrib.auth.hashers import make_password


class AddUserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, default='12345678', write_only=True)

    class Meta:
        model = User
        fields = ('password', )


class AddStudentSerializer(serializers.HyperlinkedModelSerializer):
    user = AddUserSerializer()

    class Meta:
        model = Student
        fields = ('url', 'number', 'name', 'suahours', 'grade', 'classtype', 'phone', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(
            username=validated_data['number'],
            password=make_password(user_data['password']),
        )
        student = Student.objects.create(user=user, **validated_data)
        return student


class AddSuaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sua
        fields = ('url', 'activity', 'student', 'team', 'suahours')


class AddActivitySerializer(serializers.HyperlinkedModelSerializer):
    suas = AddSuaSerializer(many=True)

    class Meta:
        model = Activity
        fields = ('url', 'title', 'detail', 'group', 'date', 'suas')

    def create(self, validated_data):
        sua_datas = validated_data.pop('suas')
        activity = Activity.objects.create(**validated_data)
        owner = validated_data['owner']
        for sua_data in sua_datas:
            sua = Sua.objects.create(owner=owner, activity=activity, **sua_data)
        return activity



class AddAppealSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Appeal
        fields = ('url','owner','student','publicity', 'content', 'status', 'is_checked', 'feedback')

    def create(self,validated_data):
        appeal = Appeal.objects.create(**validated_data)
        return appeal

class AddPublicitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publicity
        fields = ('url','owner','activity', 'title', 'content', 'contact', 'is_published', 'begin', 'end')


class AddProofSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Proof
        fields = ('url', 'is_offline', 'proof_file')

    def is_valid(self, *args, **kwargs):
        is_valid_super = super(AddProofSerializer, self).is_valid(*args, **kwargs)
        has_upload_file = True if 'proof_file' in self.validated_data.keys() else False
        is_offline = True if self.validated_data['is_offline'] else False
        return is_valid_super and (has_upload_file or is_offline)



class AddApplicationSerializer(serializers.HyperlinkedModelSerializer):
    sua = AddSuaSerializer()
    proof = AddProofSerializer()
    class Meta:
        model = Application
        fields = ('url', 'sua', 'created','contact', 'proof')

    def create(self, validated_data):
        owner = validated_data['owner']
        sua_data = validated_data.pop('sua')
        sua = Sua.objects.create(owner=owner, **sua_data)
        proof_data = validated_data.pop('proof')
        proof = Proof.objects.create(owner=owner, **proof_data)
        application = Application.objects.create(sua=sua, proof=proof,**validated_data)
        return application
