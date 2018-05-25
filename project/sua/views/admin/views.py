from project.sua.models import Publicity
from project.sua.models import Sua
from project.sua.models import Application
from project.sua.models import Student
from project.sua.models import Activity
from project.sua.models import Appeal

from project.sua.serializers import PublicitySerializer
from project.sua.serializers import SuaSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import AppealSerializer
from project.sua.serializers import StudentSerializer
from project.sua.serializers import ActivitySerializer
from project.sua.serializers import ActivityWithSuaSerializer

from .serializers import AdminAddSuaForActivitySerializer
from .serializers import AdminApplicationSerializer
from .serializers import AdminApplicationMassageSerializer
from .serializers import SuaforApplicationsSerializer
from .serializers import ActivityForAdminSerializer
from .serializers import AdminPublicitySerializer
from .serializers import AdminAppealSerializer
from .serializers import AdminActivitySerializer

from project.sua.views.utils.base import BaseView
from project.sua.views.utils.mixins import NavMixin
import project.sua.views.utils.tools as tools

from .serializers import PublicityWithActivitySerializer

from project.sua.permissions import IsAdminUserOrActivity

from django.http import HttpResponseRedirect, Http404


class IndexView(BaseView, NavMixin):
    template_name = 'sua/adminindex.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        serialized = super(IndexView, self).serialize(request)
        # print(request.GET)
#        if request.GET is not None:
#            grade = request.GET['grade']
#            classtype = request.GET['classtype']
#            classtype = str(classtype)+'班'
#            student_set = Student.objects.filter(deletedAt=None,grade=grade,classtype=classtype).order_by('number')
#        else:
        deleteds = {}
        student_set = Student.objects.filter(deletedAt=None).order_by('number')  # 获取所有学生信息
        student_data = StudentSerializer(  # 序列化所有学生信息
            student_set,
            many=True,
            context={'request': request}
        )

        deleteds['students'] = tools.get_deleteds(Student, StudentSerializer, request)

        appeal_set = Appeal.objects.filter(deletedAt=None).order_by(
            'is_checked', '-created')  # 获取在公示期内的所有申诉
        appeal_data = AppealSerializer(  # 序列化申诉
            appeal_set,
            many=True,
            context={'request': request}
        )
        appeals = appeal_data.data
        for appeal in appeals:
            appeal['created'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(appeal['created']))

        deleteds['appeals'] = tools.get_deleteds(Appeal, AppealSerializer, request)

        application_set = Application.objects.filter(deletedAt=None).order_by('is_checked', '-created')# 获取所有申请,按时间的倒序排序
        application_data = ApplicationSerializer(  # 序列化所有申请
            application_set,
            many=True,
            context={'request': request}
        )
        applications = application_data.data
        for application in applications:
            application['created'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(application['created']))

        deleteds['applications'] = tools.get_deleteds(Application, ApplicationSerializer, request)

        activity_set = Activity.objects.filter(
            deletedAt=None).order_by('-created')  # 获取所有当前管理员创建的活动
        activity_data = ActivityForAdminSerializer(  # 序列化所有所有当前管理员创建的活动
            activity_set,
            many=True,
            context={'request': request}
        )

        deleteds['activities'] = tools.get_deleteds(Activity, ActivitySerializer, request)

        activities = activity_data.data
        for activity in activities:
            activity['date'] = tools.Date2String_SHOW(
                tools.TZString2DateTime(activity['date']))
            for publicity in activity['publicities']:
                publicity['begin'] = tools.DateTime2String_SHOW(
                    tools.TZString2DateTime(publicity['begin']))
                publicity['end'] = tools.DateTime2String_SHOW(
                    tools.TZString2DateTime(publicity['end']))

        # deleteds.sort(key=tools.sort_by_deletedAt, reverse=True)

        # print(deleteds)


        serialized.update({
            'appeals': appeals,
            'applications': applications,
            'students': student_data.data,
            'activities': activities,
            'deleteds': deleteds,
        })
        return serialized
    def deserialize(self, request, *args, **kwargs):
        merge_applications = []
        applications = Application.objects.filter(deletedAt=None,).all()
        for application in applications:
            if str(application.id) in request.data:
                merge_applications.append(application)
        if 'activity_id' in request.data:
            activity = Activity.objects.filter(id=request.data['activity_id'],deletedAt=None).get()
        elif bool(merge_applications):
            activity = merge_applications[0].sua.activity
        print(activity)
        for i in range(len(merge_applications)):
            sua = Sua.objects.filter(deletedAt=None,application=merge_applications[i]).update(activity=activity)
            print(sua)
            #sua.save(activity=activity)
            #else:
                #return False

        self.url="/admin"
        return True

class AppealView(BaseView, NavMixin):
    template_name = 'sua/admin_appeal.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        appeal_id = kwargs['pk']
        serialized = super(AppealView, self).serialize(request)
        appeal = Appeal.objects.filter(deletedAt=None,id=appeal_id).get()
        appeal_data = AdminPublicitySerializer(
            appeal,
            context={'request': request}
        )

        activity = appeal.publicity.activity
        sua_set = activity.suas.filter(
            student=appeal.student,
            application=None,
            deletedAt=None,
        )
        if len(sua_set) == 0:
            sua = None
        else:
            sua = sua_set[0]
        sua_data = SuaSerializer(
            sua,
            context={'request': request}
        )

        serializer = AdminAppealSerializer(
            Appeal.objects.filter(deletedAt=None,id=appeal_id).get(),
            context={'request': request}
        )
        serialized.update({
            'serializer': serializer,
            'appeal': appeal_data.data,
            'sua': sua_data.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        appeal_id = kwargs['pk']
        serializer = AdminAppealSerializer(
            Appeal.objects.filter(deletedAt=None,id=appeal_id).get(),
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
            Application.objects.filter(deletedAt=None,id=application_id).get(),
            context={'request': request}
        )

        sua_set = Sua.objects.filter(
            application__id=application_id,
            deletedAt=None,
        )[0]

        sua_data = SuaSerializer(
            sua_set,
            context={'request': request}
        )
        serializer = AdminApplicationSerializer(
            Application.objects.filter(deletedAt=None,id=application_id).get(),
            context={'request': request}
        )
        serialized.update({
            'serializer': serializer,
            'application': application_data.data,
            'sua': sua_data.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        application_id = kwargs['pk']
        sua_data = SuaforApplicationsSerializer(
            Sua.objects.filter(
                application__id=application_id,
                deletedAt=None,
            ).get(),
            data=request.data,
            context={'request': request},
        )

        serializer = AdminApplicationSerializer(
            Application.objects.filter(deletedAt=None,id=application_id).get(),
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


class PublicityView(BaseView, NavMixin):
    template_name = 'sua/admin_publicity.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        activity_id = kwargs['pk']
        activity = Activity.objects.filter(deletedAt=None,id=activity_id).get()
        activity_data = ActivitySerializer(
            instance=activity,
            context={'request': request}
        )
        serialized = super(PublicityView, self).serialize(request)
        serializer = PublicityWithActivitySerializer(
            context={'request': request})
        serialized.update({
            'activity': activity_data.data,
            'serializer': serializer,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        activity_id = kwargs['pk']
        serializer = PublicityWithActivitySerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(activity=Activity.objects.filter(deletedAt=None,
                id=activity_id).get(), owner=user)
            self.url = '/admin/publicities/%s/manage/' % activity_id
            return True
        else:
            print(serializer.errors)
            return False


class ChangePublicityView(BaseView, NavMixin):
    template_name = 'sua/admin_publicity.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        publicity_id = kwargs['pk']
        publicity = Publicity.objects.filter(deletedAt=None,id=publicity_id).get()
        activity = publicity.activity
        serialized = super(ChangePublicityView, self).serialize(request)
        serializer = PublicityWithActivitySerializer(
            instance=publicity,
            context={'request': request}
        )
        extra_data = {}
        extra_data['begin'] = tools.DateTime2String_VALUE(
            tools.TZString2DateTime(serializer.data['begin'])
        )
        extra_data['end'] = tools.DateTime2String_VALUE(
            tools.TZString2DateTime(serializer.data['end'])
        )
        serialized.update({
            'activity': activity,
            'serializer': serializer,
            'extra_data': extra_data
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        publicity_id = kwargs['pk']
        publicity = Publicity.objects.filter(deletedAt=None,id=publicity_id).get()
        serializer = PublicityWithActivitySerializer(
            instance=publicity,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            self.url = '/admin/publicities/%s/manage/' % publicity.activity.id
            return True
        else:
            return False


class ManagePublicityView(BaseView, NavMixin):
    template_name = 'sua/admin_publicity_manage.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        activity_id = kwargs['pk']
        activity = Activity.objects.filter(deletedAt=None,id=activity_id).get()
        serialized = super(ManagePublicityView, self).serialize(request)
        publicity_set = Publicity.objects.filter(  # 获取该活动的所有公示
            deletedAt=None,
            activity=activity
        ).order_by('-is_published', '-created')
        publicity_data = PublicitySerializer(  # 序列化公示
            publicity_set,
            many=True,
            context={'request': request}
        )
        for publicity in publicity_data.data:
            publicity['created'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(publicity['created']))
            publicity['begin'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(publicity['begin']))
            publicity['end'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(publicity['end']))

        serialized.update({
            'activity': activity,
            'publicities': publicity_data.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        activity_id = kwargs['pk']
        publicities = PublicitySerializer(
            data=request.data, context={'request': request})
        if publicities.is_valid():

            publicities.save(activity=Activity.objects.filter(deletedAt=None,
                id=activity_id).get(), owner=user)
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
        activity = Activity.objects.filter(deletedAt=None,id=activity_id).get()
        serialized = super(AddSuaForActivityView, self).serialize(request)
        activitySerializer = ActivityWithSuaSerializer(
            activity,
            context={'request': request}
        )
        students = []
        filter_students = []
        for sua in activity.suas.filter(deletedAt=None):
            filter_students.append(sua.student)
        for student in Student.objects.filter(deletedAt=None):
            if student not in filter_students:
                studentSerializer = StudentSerializer(
                    instance=student,
                    context={'request': request}
                )
                students.append(studentSerializer.data)

        # print(students)

        suaSerializer = AdminAddSuaForActivitySerializer(
            context={'request': request})
        serialized.update({
            'activity': activitySerializer.data,
            'serializer': suaSerializer,
            'students': students,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        activity_id = kwargs['pk']
        activity = Activity.objects.filter(deletedAt=None,id=activity_id).get()
        activitySerializer = ActivitySerializer(
            activity,
            context={'request': request}
        )
        suaSerializer = AdminAddSuaForActivitySerializer(
            data=request.data,
            context={'request': request},
        )
        if suaSerializer.is_valid():
            if((request.user.is_staff) or (request.user.student.power == 1 and activity.owner == request.user)):
                suaSerializer.save(
                    owner=user,
                    activity=activity,
                    is_valid=True
                    )
                self.url = activitySerializer.data['url']
                return True
        else:
            return False


class ChangeSuaForActivityView(BaseView, NavMixin):
    template_name = 'sua/admin_sua_add.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        sua_id = kwargs['pk']
        sua = Sua.objects.filter(deletedAt=None,id=sua_id).get()
        students = [StudentSerializer(
            instance=sua.student,
            context={'request': request}
        ).data]
        serialized = super(ChangeSuaForActivityView, self).serialize(request)
        activitySerializer = ActivityWithSuaSerializer(
            sua.activity,
            context={'request': request}
        )
        suaSerializer = AdminAddSuaForActivitySerializer(
            instance=sua,
            context={'request': request}
        )
        serialized.update({
            'activity': activitySerializer.data,
            'serializer': suaSerializer,
            'students': students,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        sua_id = kwargs['pk']
        sua = Sua.objects.filter(deletedAt=None,id=sua_id).get()
        activitySerializer = ActivitySerializer(
            sua.activity,
            context={'request': request}
        )
        suaSerializer = AdminAddSuaForActivitySerializer(
            instance=sua,
            data=request.data,
            context={'request': request},
        )
        if suaSerializer.is_valid():
            if((request.user.is_staff) or (request.user.student.power == 1 and activity.owner == request.user)):
                suaSerializer.save()
                self.url = activitySerializer.data['url']
                return True
        else:
            return False

def CheckTheActivityView(request, *args, **kwargs):
    activity_id = kwargs['pk']
    activity = Activity.objects.filter(deletedAt=None,id=activity_id).get()
    activitySerializer = AdminActivitySerializer(
        activity,
        context={'request': request}
    )
    if(request.user.is_staff):
        if(activity.is_valid == True):
            activity.is_valid=False
        else:
            activity.is_valid=True
        activity.save()
    return HttpResponseRedirect(activitySerializer.data['url'])

def CheckTheSuaView(request, *args, **kwargs):
    url = request.GET['url']
    sua_id = kwargs['pk']
    sua = Sua.objects.filter(deletedAt=None,id=sua_id).get()
    if(request.user.is_staff or request.user.student.power == 1):
        if(sua.is_valid == True):
            sua.is_valid=False
        else:
            sua.is_valid=True
        sua.save()
    return HttpResponseRedirect(url)



class ApplicationsMergeView(BaseView, NavMixin):
    template_name = 'sua/applications_activity_merge.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        activities_data = ActivityWithSuaSerializer(
            Activity.objects.filter(deletedAt=None,owner=request.user).order_by('id'),
            many=True,
            context={'request':request},
            )
        application_set = Application.objects.filter(deletedAt=None).order_by('created')# 获取所有申请,按时间的倒序排序
        applications_data = ApplicationSerializer(  # 序列化所有申请
            application_set,
            many=True,
            context={'request':request},
            )
        serialized = super(ApplicationsMergeView, self).serialize(request)
        serialized.update({
            'activities': activities_data.data,
            'applications': applications_data.data,
        })

        return serialized

    def deserialize(self, request, *args, **kwargs):
        merge_applications = []
        sua_students = []
        applications = Application.objects.filter(deletedAt=None,).all()
        for application in applications:
            if str(application.id) in request.data:
                merge_applications.append(application)
        if 'activity_id' in request.data:
            activity = Activity.objects.filter(id=request.data['activity_id'],deletedAt=None).get()
        elif bool(merge_applications):
            activity = merge_applications[0].sua.activity
        activity_suas = Sua.objects.filter(deletedAt=None, activity=activity).all()
        for sua in activity_suas:
            if sua.student not in sua_students:
                sua_students.append(sua.student)
        for i in range(len(merge_applications)):
            sua = Sua.objects.filter(deletedAt=None,application=merge_applications[i]).get()
            old_activity = sua.activity
            if sua.student not in sua_students:
                sua_students.append(sua.student)
                Sua.objects.filter(deletedAt=None,application=merge_applications[i]).update(activity=activity)
                if old_activity != activity:
                    old_activity.delete()

        self.url="/admin"
        return True
