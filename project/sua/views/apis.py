from rest_framework import viewsets
from rest_framework import permissions
from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly

import project.sua.views.forms.serializers as firs
import project.sua.serializers as sirs

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from project.sua.models import Student,Proof,Sua,Activity,Publicity,Application,Appeal
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    student = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api-student-detail',
    )
    class Meta:
        model = User
        fields = ('url', 'student', 'username', 'is_staff', 'password', 'groups', 'applications', )
        extra_kwargs = {
            'url':{'view_name': 'api-user-detail'},
        }

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'suagroup', 'name', 'user_set')

class ApplicationWithStudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ('url',)
        extra_kwargs = {
            'url':{'view_name': 'api-application-detail'},
        }

class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = ('url', 'user', 'name', 'number', 'suahours', 'grade', 'classtype', 'phone', 'suas', 'appeals',)
        extra_kwargs = {
            'url':{'view_name': 'api-student-detail'},
            'appeals':{'view_name':'api-appeal-detail'},
            'suas':{'view_name':'api-sua-detail'},
        }
class ActivitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('url', 'title', 'date', 'detail', 'group', 'is_valid', 'suas', 'publicities', 'id')
        extra_kwargs = {
            'url':{'view_name': 'api-activity-detail'},
            'suas':{'view_name':'api-sua-detail'},
            'publicities':{'view_name':'api-publicity-detail'},
        }

class ProofSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proof
        fields = ('url', 'is_offline', 'proof_file', 'applications')
        extra_kwargs = {
            'url':{'view_name': 'api-proof-detail'},
            'applications':{'view_name':'api-application-detail'},
        }

class SuaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sua
        fields = ('url', 'student', 'activity', 'team', 'suahours', 'application', 'is_valid',)
        extra_kwargs = {
            'url':{'view_name': 'api-sua-detail'},
            'activity':{'view_name': 'api-activity-detail'},
            'student':{'view_name': 'api-student-detail'},
            'application':{'view_name': 'api-application-detail'},
        }
        
class PublicitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publicity
        fields = ('url','id', 'activity', 'title', 'content', 'is_published', 'begin', 'end', 'appeals')
        extra_kwargs = {
            'url':{'view_name': 'api-publicity-detail'},
            'activity':{'view_name': 'api-activity-detail'},
            'appeals':{'view_name': 'api-appeal-detail'},
        }
        
class ApplicationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Application
        fields = ('url', 'created', 'contact', 'sua', 'proof', 'is_checked', 'status', 'feedback', 'id',)
        extra_kwargs = {
            'url':{'view_name': 'api-application-detail'},
            'sua':{'view_name': 'api-sua-detail'},
            'proof':{'view_name':'api-proof-detail'},
        }

class AppealSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Appeal
        fields = ('url', 'created', 'student', 'publicity', 'content', 'is_checked', 'status', 'feedback', 'id')
        extra_kwargs = {
            'url':{'view_name': 'api-appeal-detail'},
            'student':{'view_name': 'api-student-detail'},
            'publicity':{'view_name': 'api-publicity-detail'},
        }
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
class PublicityViewSet(viewsets.ModelViewSet):
    queryset = Publicity.objects.all()
    serializer_class = PublicitySerializer
    
class SuaViewSet(viewsets.ModelViewSet):
    queryset = Sua.objects.all()
    serializer_class = SuaSerializer
    
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    
class AppealViewSet(viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
    
class ProofViewSet(viewsets.ModelViewSet):
    queryset = Proof.objects.all()
    serializer_class = ProofSerializer
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                username = User.objects.get(username=serializer.validated_data['username']).username
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            user = authenticate(request, username=username, password=serializer.validated_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    userSerializer = UserSerializer(user, context={'request': request})
                    return Response(userSerializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)