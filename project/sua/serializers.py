from django.contrib.auth.models import User, Group
from project.sua.models import Student, SuaGroup, Sua, Application, Activity, Publicity, Appeal, Proof

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('url', 'id', 'student', 'username', 'is_staff', 'password', 'groups', 'applications', )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'suagroup', 'name', 'user_set')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('url', 'user', 'name', 'number', 'suahours', 'totalhours', 'grade', 'classtype', 'phone', 'suas', 'appeals', 'id', 'power', 'deleted_by')


class SuaGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuaGroup
        fields = ('url', 'id', 'group', 'name', 'is_staff', 'contact', 'rank')


class FilterIsPublishedListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(deleted_at=None,is_published=True)
        return super(FilterIsPublishedListSerializer, self).to_representation(data)


class PublicityWithActivitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Publicity
        list_serializer_class = FilterIsPublishedListSerializer
        fields = ('url', 'id', 'created', 'title', 'content', 'contact', 'is_published', 'begin', 'end' )


class ActivityForAdminSerializer(serializers.HyperlinkedModelSerializer):
    publicities = PublicityWithActivitySerializer(many=True)

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities', 'id')


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    #publicities = PublicityWithActivitySerializer()

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities', 'id', 'is_created_by_student', 'deleted_by')

class ProofSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proof
        fields = ('url', 'is_offline', 'proof_file', 'applications')

class SuaSerializer(serializers.HyperlinkedModelSerializer):
    activity = ActivitySerializer()
    student = StudentSerializer()

    class Meta:
        model = Sua
        fields = ('url', 'id', 'student', 'activity', 'team', 'suahours', 'application', 'is_valid',)


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
        fields = ('url', 'title', 'date', 'detail', 'group', 'suas', 'id')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    sua = SuaSerializer()
    class Meta:
        model = Application
        fields = ('url', 'created', 'contact', 'sua', 'proof', 'is_checked', 'status', 'feedback', 'id', 'deleted_by')


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
        fields = ('url', 'created', 'student', 'publicity', 'content', 'is_checked', 'status', 'feedback', 'id', 'deleted_by')


class AddAppealSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Appeal
        fields = ('url', 'content',)

class ActivityforApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid','id')
