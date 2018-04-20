from rest_framework import serializers
from project.sua.serializers import PublicityWithActivitySerializer
from project.sua.models import Activity

class ActivityForAdminSerializer(serializers.HyperlinkedModelSerializer):
    publicities = PublicityWithActivitySerializer(many=True)

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities', 'id')
