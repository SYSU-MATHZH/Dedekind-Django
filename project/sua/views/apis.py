from rest_framework import viewsets
from rest_framework import permissions
from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly

from project.sua.models import Sua, Proof, Application, Publicity, Activity, Student, Appeal, SuaGroup

import project.sua.views.forms.serializers as firs
import project.sua.serializers as sirs

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = firs.AddStudentSerializer
    
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = firs.AddActivitySerializer
    
class PublicityViewSet(viewsets.ModelViewSet):
    queryset = Publicity.objects.all()
    serializer_class = firs.AddPublicitySerializer
    
class SuaViewSet(viewsets.ModelViewSet):
    queryset = Sua.objects.all()
    serializer_class = firs.AddSuaSerializer
    
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = firs.AddApplicationSerializer
    
class AppealViewSet(viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = firs.AddAppealSerializer
    
class ProofViewSet(viewsets.ModelViewSet):
    queryset = Proof.objects.all()
    serializer_class = firs.AddProofSerializer