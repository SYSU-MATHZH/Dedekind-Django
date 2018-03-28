from django.utils import timezone
from django.http import HttpResponse


from project.sua.models import Publicity
from project.sua.models import Sua
from project.sua.models import Application
from project.sua.models import Student
from project.sua.models import Activity
from project.sua.models import Appeal
from project.sua.models import Proof


from project.sua.serializers import PublicitySerializer
from project.sua.serializers import SuaSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import AppealSerializer
from project.sua.serializers import AddAppealSerializer
from project.sua.serializers import AppealSerializer
from project.sua.serializers import StudentSerializer
from project.sua.serializers import ActivitySerializer
from project.sua.serializers import AppealSerializer
from project.sua.serializers import AdminAppealSerializer
from project.sua.serializers import AdminPublicitySerializer
from project.sua.serializers import AdminApplicationSerializer
from project.sua.serializers import ActivityWithSuaSerializer
from project.sua.serializers import ProofSerializer

from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.mixins import ListModelMixin

from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly
import project.sua.serializers as sirs
import project.sua.views.forms.serializers as firs
import project.sua.views.forms.mixins as mymixins


from .utils.base import BaseView
from .utils.mixins import NavMixin

from .forms.serializers import AddStudentSerializer,AddPublicitySerializer

class IndexView(BaseView, NavMixin):
    template_name = 'sua/adminindex.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        serialized = super(IndexView, self).serialize(request)

        student_set = Student.objects.filter().order_by('number')  #获取所有学生信息
        student_data = StudentSerializer(  # 序列化所有学生信息
            student_set,
            many=True,
            context={'request':request}
        )

        appeal_set = Appeal.objects.filter().order_by('created')  # 获取在公示期内的所有公示
        appeal_data = AppealSerializer(  # 序列化公示
            appeal_set,
            many=True,
            context={'request': request}
        )

        application_set = Application.objects.filter(  #获取所有申请,
        ).order_by('-created')                      # 按时间的倒序排序
        application_data = ApplicationSerializer(  # 序列化所有申请
            application_set,
            many=True,
            context={'request': request}
        )

        activity_set = Activity.objects.filter()  # 获取所有活动
        activity_data = ActivitySerializer(  # 序列化所有活动
            activity_set,
            many=True,
            context={'request': request}
        )
        publicity_set = Publicity.objects.filter(
            begin__lte=timezone.now(),
            end__gte=timezone.now()
        ).order_by('begin')
        publicity_data = PublicitySerializer(
            publicity_set,
            many=True,
            context={'request': request}
        )
        serialized.update({
            'appeals': appeal_data.data,
            'applications': application_data.data,
            'students':student_data.data,
            'activities':activity_data.data,
            'publicities':publicity_data.data,
        })
        return serialized

class AppealView(BaseView, NavMixin):
    template_name = 'sua/admin_appeal.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        appeal_id = kwargs['pk']
        serialized = super(AppealView, self).serialize(request)

        appeal_data = AdminPublicitySerializer(
            Appeal.objects.get(id=appeal_id),
            context = {'request':request}
        )

        activity = Activity.objects.filter(
            title = appeal_data.data['publicity']['activity']['title']
            ).get()
        sua_set = activity.suas.filter(
            student__number = appeal_data.data['student']['number'],
            activity__title = appeal_data.data['publicity']['activity']['title'],
            ).get() 
        sua_data = SuaSerializer(
            sua_set,
            context = {'request':request}
        )

        serializer = AdminAppealSerializer(
            Appeal.objects.get(id=appeal_id),
            context={'request':request}
        )
        serialized.update({
            'serializer': serializer,
            'appeal':appeal_data.data,
            'sua':sua_data.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        appeal_id = kwargs['pk']
        serializer = AdminAppealSerializer(
            Appeal.objects.get(id = appeal_id),
            data=request.data,
            context={'request': request}
            )
        if serializer.is_valid():
            serializer.save(is_checked=True)
            self.url = serializer.data['url']
            return True
        else:
            return False

class ApplicationView(BaseView, NavMixin):
    template_name = 'sua/admin_application.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        applicaiton_id = kwargs['pk']
        serialized = super(ApplicationView, self).serialize(request)

        application_data = AdminApplicationSerializer(
            Application.objects.get(id=applicaiton_id),
            context = {'request':request}
        )

#        activity_set = Activity.objects.get(id=applicaiton_id)
#        Activity_data = ActivityWithSuaSerializer(
#            activity_set,
#            context = {'request':request}
#        )
#        proof_set = Proof.objects.get(id=applicaiton_id)
#        proof_data = ProofSerializer(
#            proof_set,
#            context = {'request':request}
#        )

        serializer = AdminApplicationSerializer(
            Application.objects.get(id=applicaiton_id),
            context={'request':request}
        )
        serialized.update({
            'serializer': serializer,
            'application':application_data.data,
            #'sua':sua_data.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        application_id = kwargs['pk']
        application_set = Application.objects.get(id = application_id)
        serializer = AdminApplicationSerializer(
            application_set,
            data=request.data,
            context={'request': request},
            )
        if serializer.is_valid():
            serializer.save(is_checked=True)
#            is_checked = True,
#            publicity=appeal.publicity,
#            student = appeal.student,
#            owner=Appeal.objects.get(id=appeal_id).owner
            self.url = serializer.data['url']
            return True
        else:
            return False
