from rest_framework import serializers
from project.sua.serializers import PublicityWithActivitySerializer
from project.sua.serializers import PublicitySerializer
from project.sua.serializers import StudentSerializer
from project.sua.serializers import SuaSerializer
from project.sua.models import Activity, Appeal, Proof, Sua, Application, Publicity,Student

class ActivityForAdminSerializer(serializers.HyperlinkedModelSerializer):
    publicities = PublicityWithActivitySerializer(many=True)

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities', 'id')


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


class SuaforApplicationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sua
        fields = ('url', 'is_valid')


class AdminApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ('url', 'status','feedback', )

#class studentwithnumberSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Student
#        fields = ('name','number')
class AdminAddSuaForActivitySerializer(serializers.HyperlinkedModelSerializer):
#    students = studentwithnumberSerializer()
    class Meta:
        model = Sua
        fields = ('url', 'student', 'team', 'suahours',)



class AdminActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('url', 'is_valid')
