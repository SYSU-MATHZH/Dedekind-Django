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


class ActivitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities', 'id')


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
        fields = ('url','id', 'activity', 'title', 'content', 'is_published', 'begin', 'end', 'appeals')


class AppealSerializer(serializers.HyperlinkedModelSerializer):
    publicity = PublicitySerializer()
    student = StudentSerializer()

    class Meta:
        model = Appeal
        fields = ('url', 'created', 'student', 'publicity', 'content', 'is_checked', 'status', 'feedback', 'id')


class ProofSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proof
        fields = ('url', 'is_offline', 'proof_file', 'applications')

class AddAppealSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Appeal
        fields = ('url', 'content',)

class ActivityforApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid','id')

#class SuaforApplicationsSerializer(serializers.ModelSerializer):
#    student = StudentNameNumberSerializer()
#    activity = ActivityforApplicationsSerializer()
#    class Meta:
#        model = Sua
#        fields = ('student', 'activity', 'suahours', 'id')

#class ProofforApplicationsSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Proof
#        fields = ('url', 'is_offline', 'proof_file')

class AdminApplicationSerializer(serializers.HyperlinkedModelSerializer):
#    proof = ProofforApplicationsSerializer()
#    sua = SuaforApplicationsSerializer()
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


class ActivityForAddApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('url', 'title', 'detail', 'group', 'date')



class SuaForAddApplicationsSerializer(serializers.HyperlinkedModelSerializer):
    activity = ActivityForAddApplicationsSerializer()


    class Meta:
        model = Sua
        fields = ('url', 'activity', 'team', 'suahours')

    # def create(self, validated_data):
    #     owner = validated_data['owner']
    #     activity_data = validated_data.pop('activity')
    #     activity = Activity.objects.create(owner=owner, **activity_data)
    #     sua = Sua.objects.create(owner=owner, activity=activity, **validated_data)
    #     return sua


class ProofForAddApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Proof
        fields = ('url', 'is_offline', 'proof_file')


class AddApplicationsSerializer(serializers.HyperlinkedModelSerializer):
    sua = SuaForAddApplicationsSerializer()
    proof = ProofForAddApplicationsSerializer()


    class Meta:
        model = Application
        fields = ('url', 'contact', 'sua', 'proof')


    def create(self, validated_data):
        owner = validated_data['owner']
        # activity = ActivityForAddApplicationsSerializer()
        # sua = SuaForAddApplicationsSerializer()
        # proof = ProofForAddApplicationsSerializer()

        sua_data = validated_data.pop('sua')
        activity_data = sua_data.pop('activity')
        activity = Activity.objects.create(owner=owner, **activity_data)
        sua = Sua.objects.create(owner=owner, activity=activity, **sua_data)
        proof_data = validated_data.pop('proof')
        proof = Proof.objects.create(owner=owner, **proof_data)
        application = Application.objects.create(owner=owner, sua=sua, proof=proof, **validated_data)
        return application


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
