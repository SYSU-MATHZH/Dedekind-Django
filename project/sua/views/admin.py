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
from project.sua.serializers import ActivityForAdminSerializer
from project.sua.serializers import ActivityWithSuaSerializer
from project.sua.serializers import AdminAddSuaForActivitySerializer
from project.sua.serializers import AppealSerializer
from project.sua.serializers import AdminAppealSerializer
from project.sua.serializers import AdminPublicitySerializer
from project.sua.serializers import AdminApplicationSerializer
from project.sua.serializers import ProofSerializer
from project.sua.serializers import AdminApplicationMassageSerializer
from project.sua.serializers import SuaforApplicationsSerializer
from project.sua.serializers import StudentNameNumberSerializer

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

from .forms.serializers import AddStudentSerializer, AddPublicitySerializer, PublicityWithActivitySerializer

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

        appeal_set = Appeal.objects.filter().order_by('created')  # 获取在公示期内的所有申诉
        appeal_data = AppealSerializer(  # 序列化申诉
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

        activity_set = Activity.objects.filter(owner=request.user)  # 获取所有当前管理员创建的活动
        activity_data = ActivityForAdminSerializer(  # 序列化所有所有当前管理员创建的活动
            activity_set,
            many=True,
            context={'request': request}
        )
        serialized.update({
            'appeals': appeal_data.data,
            'applications': application_data.data,
            'students':student_data.data,
            'activities':activity_data.data,
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
        appeal = Appeal.objects.get(id=appeal_id)
        appeal_data = AdminPublicitySerializer(
            appeal,
            context = {'request':request}
        )

        activity = appeal.publicity.activity
        sua_set = activity.suas.filter(
            student=appeal.student,
            application=None,
            )
        if len(sua_set) == 0:
            sua = None
        else:
            sua = sua_set[0]
        sua_data = SuaSerializer(
            sua,
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
        application_id = kwargs['pk']
        serialized = super(ApplicationView, self).serialize(request)

        application_data = AdminApplicationMassageSerializer(
            Application.objects.get(id=application_id),
            context = {'request':request}
        )
        sua_set = Sua.objects.filter(
            application__id = application_id,
        ).get()
        sua_data = SuaSerializer(
            sua_set,
            context = {'request':request}
        )
        serializer = AdminApplicationSerializer(
            Application.objects.get(id=application_id),
            context={'request':request}
        )
        serialized.update({
            'serializer': serializer,
            'application':application_data.data,
            'sua':sua_data.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        application_id = kwargs['pk']
        application_data = AdminApplicationMassageSerializer(
            Application.objects.get(id=application_id),
            context = {'request':request}
        )
        sua_data = SuaforApplicationsSerializer(
            Sua.objects.filter(
                application__id = application_id,
            ).get(),
            data=request.data,
            context={'request': request},
        )

        serializer = AdminApplicationSerializer(
            Application.objects.get(id=application_id),
            data=request.data,
            context={'request': request},
            )
        if serializer.is_valid() and sua_data.is_valid():
            serializer.save(is_checked=True)
            sua_data.save(is_valid=True)
            self.url = serializer.data['url']
            return True
        else:
            return False

class PublicityView(BaseView,NavMixin):
    template_name = 'sua/admin_publicity.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        activity_id = kwargs['pk']
        activity = Activity.objects.get(id=activity_id)
        serialized = super(PublicityView, self).serialize(request)
        serializer = PublicityWithActivitySerializer(context={'request':request})
        serialized.update({
            'activity': activity,
            'serializer': serializer,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        activity_id = kwargs['pk']
        serializer = PublicityWithActivitySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():

            serializer.save(activity=Activity.objects.get(id=activity_id), owner=user)
            self.url = serializer.data['url']
            return True
        else:
            return False


class ManagePublicityView(BaseView,NavMixin):
    template_name = 'sua/admin_publicity_manage.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        activity_id = kwargs['pk']
        activity = Activity.objects.get(id=activity_id)
        serialized = super(ManagePublicityView, self).serialize(request)
        publicity_set = Publicity.objects.filter(  # 获取该活动的所有公示
            # is_published=True,
            # begin__lte=timezone.now(),
            # end__gte=timezone.now(),
            activity=activity
        )
        publicity_data = PublicitySerializer(  # 序列化公示
            publicity_set,
            many=True,
            context={'request': request}
        )
        serialized.update({
            'activity': activity,
            'publicities': publicity_data.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        activity_id = kwargs['pk']
        publicities = PublicitySerializer(data=request.data, context={'request': request})
        if publicities.is_valid():

            publicities.save(activity=Activity.objects.get(id=activity_id), owner=user)
            self.url = publicities.data['url']
            return True
        else:
            return False


class AddSuaForActivityView(BaseView, NavMixin):
    template_name = 'sua/admin_sua_add.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        activity_id = kwargs['pk']
        activity = Activity.objects.get(id=activity_id)
        serialized = super(AddSuaForActivityView, self).serialize(request)
        activitySerializer = ActivityWithSuaSerializer(
            activity,
            context={'request': request}
        )
        suaSerializer = AdminAddSuaForActivitySerializer(context={'request': request})
        serialized.update({
            'activity': activitySerializer.data,
            'serializer': suaSerializer,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        activity_id = kwargs['pk']
        activity = Activity.objects.get(id=activity_id)
        activitySerializer = ActivitySerializer(
            activity,
            context={'request': request}
        )
        suaSerializer = AdminAddSuaForActivitySerializer(
            data=request.data,
            context={'request': request},
        )
        if suaSerializer.is_valid():
            suaSerializer.save(
                owner=user,
                activity=activity,
                is_valid=True
            )
            self.url = activitySerializer.data['url']
            return True
        else:
            return False


class Addstusuahoursview(BaseView, NavMixin):
    template_name = 'sua/addstusuahours.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        serialized = super(Addstusuahoursview, self).serialize(request)
        students_data = Student.objects.all()
        activity_set = Activity.objects.filter(owner=request.user)  # 获取所有当前管理员创建的活动
        activity_data = ActivitySerializer(  # 序列化所有所有当前管理员创建的活动
            activity_set,
            many=True,
            context={'request': request}
        )
        serialized.update({
             'students':students_data,
             'activities':activity_data.data,
        })
        return serialized
    def deserialize(self, request, *args, **kwargs):
        students_data = Student.objects.all()
        activities_data = Activity.objects.all()
        if request.POST.get("id")==None:
            return False
        else:
            activity_data = Activity.objects.filter(id=request.POST.get("id")).get()
        for na in students_data:
            if request.POST.get(('addsuahours'+str(na.id)))!="":
                suahours_data = int(request.POST.get(('addsuahours'+str(na.id))))
            else:
                return False
            if(request.POST.get('is_add'+str(na.id))):
                Sua.objects.create(owner=request.user, student=na, activity=activity_data, team=activity_data.group, suahours=suahours_data, is_valid=True)
        self.url = '/admin'
        return True
