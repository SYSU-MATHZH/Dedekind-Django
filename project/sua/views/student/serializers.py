<<<<<<< HEAD
from rest_framework import serializers
from project.sua.models import Activity, Proof, Sua, Application


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
=======
from rest_framework import serializers
from project.sua.models import Activity, Proof, Sua, Application


class DEActivityForAddApplicationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('url','title', 'detail', 'group', 'start', 'end')


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
>>>>>>> 4aeedf022c269cdd7612b09a4c4b063cbcb5fdf6
