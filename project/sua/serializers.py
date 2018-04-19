from django.contrib.auth.models import User, Group
from project.sua.models import Student, SuaGroup, Sua, Application, Activity, Publicity, Appeal, Proof

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('url', 'student', 'username', 'is_staff', 'password', 'groups', 'applications', )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'suagroup', 'name', 'user_set')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('url', 'user', 'name', 'number', 'suahours', 'grade', 'classtype', 'phone', 'suas', 'appeals', 'id')


class SuaGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuaGroup
        fields = ('url', 'group', 'name', 'is_staff', 'contact', 'rank')


class FilterIsPublishedListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_published=True)
        return super(FilterIsPublishedListSerializer, self).to_representation(data)


class PublicityWithActivitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Publicity
        list_serializer_class = FilterIsPublishedListSerializer
        fields = ('url', 'created', 'title', 'content', 'contact', 'is_published', 'begin', 'end' )


class ActivityForAdminSerializer(serializers.HyperlinkedModelSerializer):
    publicities = PublicityWithActivitySerializer(many=True)

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities', 'id')


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    #publicities = PublicityWithActivitySerializer()

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities', 'id')

class ProofSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proof
        fields = ('url', 'is_offline', 'proof_file', 'applications')

class SuaSerializer(serializers.HyperlinkedModelSerializer):
    activity = ActivitySerializer()
    student = StudentSerializer()

    class Meta:
        model = Sua
        fields = ('url', 'student', 'activity', 'team', 'suahours', 'application', 'is_valid',)


class StudentNameNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('name', 'number')


class SuaOnlySerializer(serializers.ModelSerializer):
    student = StudentNameNumberSerializer()
    class Meta:
        model = Sua
        fields = ('student', 'team', 'suahours','id')


class ActivityWithSuaSerializer(serializers.ModelSerializer):
    suas = SuaOnlySerializer(many=True)

    class Meta:
        model = Activity
        fields = ('url','title', 'date', 'detail', 'group', 'suas', 'id')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    sua = SuaSerializer()
    class Meta:
        model = Application
        fields = ('url', 'created', 'contact', 'sua', 'proof', 'is_checked', 'status', 'feedback', 'id',)


class PublicitySerializer(serializers.HyperlinkedModelSerializer):
    activity = ActivityWithSuaSerializer()

    class Meta:
        model = Publicity
        fields = ('url','id', 'activity','created', 'title', 'content', 'is_published', 'begin', 'end', 'appeals')


class AppealSerializer(serializers.HyperlinkedModelSerializer):
    publicity = PublicitySerializer()
    student = StudentSerializer()

    class Meta:
        model = Appeal
        fields = ('url', 'created', 'student', 'publicity', 'content', 'is_checked', 'status', 'feedback', 'id')


class AddAppealSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Appeal
        fields = ('url', 'content',)

class ActivityforApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid','id')

class SuaforApplicationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sua
        fields = ('url','is_valid')

class ProofforApplicationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proof
        fields = ('url', 'is_offline', 'proof_file')

class AdminApplicationMassageSerializer(serializers.HyperlinkedModelSerializer):
    proof = ProofforApplicationsSerializer()
    sua = SuaSerializer()
    class Meta:
        model = Application
        fields = ('url', 'proof', 'sua',)


class AdminAddSuaForActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sua
        fields = ('url', 'student', 'team', 'suahours')


class AdminApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ('url', 'status','feedback', )

class AdminAppealSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Appeal
        fields = ('url', 'status','feedback',)

class AdminPublicitySerializer(serializers.HyperlinkedModelSerializer):
    publicity = PublicitySerializer()
    student = StudentSerializer()

    class Meta:
        model = Appeal
        fields = ('url','content','student','publicity')


class DEActivityForAddApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('url','title', 'detail', 'group', 'date')


class DESuaForAddApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sua
        fields = ('url','team', 'suahours')


class DEProofForAddApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Proof
        fields = ('url','is_offline', 'proof_file')


class DEAddApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Application
        fields = ('url', 'contact')
