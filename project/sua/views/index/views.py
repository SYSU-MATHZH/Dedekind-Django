from project.sua.models import Publicity,Activity,Application,Student,Appeal

from project.sua.serializers import PublicitySerializer
from project.sua.serializers import SuaSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import AppealSerializer
from project.sua.serializers import AddAppealSerializer
from project.sua.serializers import ActivitySerializer
from project.sua.serializers import StudentSerializer

from project.sua.views.admin.serializers import ActivityForAdminSerializer

from project.sua.views.utils.base import BaseView
from project.sua.views.utils.mixins import NavMixin
import project.sua.views.utils.tools as tools

from django.utils import timezone
import datetime

class IndexView(BaseView, NavMixin):
    def get_template_names(self):#获取template_name

        if self.request.user.is_staff:
            return ['sua/admin/admin_index.html']
        elif self.request.user.student.power == 1:
            return ['sua/student_manager/manager_index.html']
        else:
            return ['sua/student/index.html']
    # template_name = 'sua/student/index.html'
    components = {
        'nav': 'nav',
    }


    def serialize(self, request, *args, **kwargs):
        serialized = super(IndexView, self).serialize(request)

        user = request.user
        deleteds = {}
        publicity_set = Publicity.objects.filter(  # 获取在公示期内的所有公示
            deleted_at=None,
            is_published=True,
            begin__lte=timezone.now(),
            end__gte=timezone.now()
        )
        publicity_data = PublicitySerializer(  # 序列化公示
            publicity_set,
            many=True,
            context={'request': request}
        )

        publicities = publicity_data.data
        for i in range(len(publicities)):
            publicities[i]['join_number'] = publicity_set[i].activity.number()
        for publicity in publicities:
            publicity['begin'] = tools.DateTime2String_SHOW(tools.TZString2DateTime(publicity['begin']))
            publicity['end'] = tools.DateTime2String_SHOW(tools.TZString2DateTime(publicity['end']))

        serialized.update({
            'publicities':publicities,
            })

        if user.is_staff or user.student.power == 1:

            if user.is_staff:
                application_set = Application.objects.filter(deleted_at=None).order_by('is_checked', '-created')# 获取所有申请,按时间的倒序排序
                unreviewed_applications_set = Application.objects.filter(deleted_at=None, is_checked=False).order_by('-created')# 获取未审核的申请
                unreviewed_appeals_set = Appeal.objects.filter(deleted_at=None, is_checked=False).order_by('-created')# 获取未审核的申诉
                serialized.update({
                    'ur_applications_num': len(unreviewed_applications_set),
                    'ur_appeals_num': len(unreviewed_appeals_set),
                })#获取未处理的申请和申诉的数量
            elif user.student.power == 1:
                application_set = Application.objects.filter(
                sua__activity__owner=user,
                sua__activity__is_created_by_student=False,
                deleted_at=None).order_by('-created')# 获取该学生创建的活动的申请
                unreviewed_applications_set = Application.objects.filter(
                sua__activity__owner=user,
                sua__activity__is_created_by_student=False,
                deleted_at=None,
                is_checked=False).order_by('-created')
                unreviewed_appeals_set = Appeal.objects.filter(
                publicity__activity__owner=user,
                publicity__activity__is_created_by_student=False,
                deleted_at=None,
                is_checked=False).order_by('-created')
                serialized.update({
                    'ur_applications_num': len(unreviewed_applications_set),
                    'ur_appeals_num': len(unreviewed_appeals_set),
                })#获取未处理的申请和申诉的数量

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

            if user.is_staff:
                activity_set = Activity.objects.filter(
                    deleted_at=None,
                    is_created_by_student=False,
                    ).order_by('-created')  # 获取所有当前管理员创建的活动
            elif user.student.power == 1:
                activity_set = Activity.objects.filter(
                    owner=user,
                    deleted_at=None,
                    is_created_by_student=False,
                    ).order_by('-created')                # 获取该活动级管理员创建的活动

            activity_data = ActivityForAdminSerializer(  # 序列化所有所有当前管理员创建的活动
                activity_set,
                many=True,
                context={'request': request}
            )

            activities = activity_data.data
            for activity in activities:
                activity['date'] = tools.Date2String_SHOW(
                    tools.TZString2DateTime(activity['date']))
                for publicity in activity['publicities']:
                    publicity['begin'] = tools.DateTime2String_SHOW(
                        tools.TZString2DateTime(publicity['begin']))
                    publicity['end'] = tools.DateTime2String_SHOW(
                        tools.TZString2DateTime(publicity['end']))
            deleteds['activities'] = tools.get_deleteds(Activity, ActivitySerializer, request)

            serialized.update({
                'admin_applications':applications,
                'admin_activities':activities,
            })

        if user.is_staff:
            classtypes =set([])
            grades =set([])
            student_all = Student.objects.filter(deleted_at=None,).order_by('number') #获取所有学生
            for student in student_all:
                classtypes.add(student.classtype)
                grades.add(student.grade)

            if 'classtype' and 'grade' in request.GET:
                classtype = request.GET.get('classtype')
                grade = request.GET.get('grade')
                student_set = Student.objects.filter(deleted_at=None,classtype=classtype,grade=grade).order_by('number')
            else:
                student_set = Student.objects.filter(deleted_at=None,).order_by('number')  # 获取筛选的学生

            student_data = StudentSerializer(  # 序列化所有学生信息
                student_set,
                many=True,
                context={'request': request}
            )

            deleteds['students'] = tools.get_deleteds(Student, StudentSerializer, request)

            appeal_set = Appeal.objects.filter(deleted_at=None).order_by(
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

            serialized.update({
                'admin_appeals': appeals,
                'admin_students': student_data.data,
                'classtypes':classtypes,
                'grades':grades,
            })

        if hasattr(user,'student'):

            student = user.student

            application_data = ApplicationSerializer(  # 序列化当前用户的所有申请
                user.applications.filter(deleted_at=None).order_by('-created'),
                many=True,
                context={'request': request}
            )

            applications = application_data.data
            for application in applications:
                application['created'] = tools.DateTime2String_SHOW(tools.TZString2DateTime(application['created']))

            if 'year_begin' not in request.GET:
                sua_data = SuaSerializer(  # 序列化当前学生的所有公益时记录
                    student.suas.filter(deleted_at=None,is_valid=True,activity__is_valid=True),
                    many=True,
                    context={'request': request}
                )
            else:
                year_begin = int(request.GET['year_begin'])
                year_end = int(request.GET['year_end'])
                start_date = datetime.date(year_begin, 8, 1)
                end_date = datetime.date(year_end, 8, 1)
                sua_data = SuaSerializer(# 序列化当前学生的某段学年的公益时记录
                    student.suas.filter(deleted_at=None,is_valid=True,
                        activity__is_valid=True,
                        activity__date__range=(start_date, end_date)
                    ),
                    many=True,
                    context={'request': request}
                )
                serialized.update({
                    'year_begin':year_begin,
                    'year_end':year_end
                })
            suas = sua_data.data
            # print(suas)
            for sua in suas:
                sua['activity']['date'] = tools.Date2String_SHOW(tools.TZString2Date(sua['activity']['date']))
            join_suas_number = 0#获取学生参与活动数
            for sua in suas:
                if sua['is_valid']:
                    join_suas_number += 1

            appeal_data = AppealSerializer(  # 序列化当前学生的所有申诉
                student.appeals.filter(deleted_at=None),
                many=True,
                context={'request': request}
            )

            appeals = appeal_data.data
            for appeal in appeals:
                appeal['created'] = tools.DateTime2String_SHOW(tools.TZString2DateTime(appeal['created']))

            serialized.update({
                'applications': applications,
                'suas': sua_data.data,
                'appeals': appeal_data.data,
                'join_suas_number': join_suas_number,
            })
        serialized.update({
            'deleteds': deleteds,
        })
        return serialized

        # def deserialize(self, request, *args, **kwargs):
        #     if request.user.is_staff:
        #         merge_applications = []
        #         applications = Application.objects.filter(deleted_at=None,).all()
        #         for application in applications:
        #             if str(application.id) in request.data:
        #                 merge_applications.append(application)
        #         if 'activity_id' in request.data:
        #             activity = Activity.objects.filter(id=request.data['activity_id'],deleted_at=None).get()
        #         elif bool(merge_applications):
        #             activity = merge_applications[0].sua.activity
        #         #print(activity)
        #         for i in range(len(merge_applications)):
        #             sua = Sua.objects.filter(deleted_at=None,application=merge_applications[i]).update(activity=activity)
        #         #    print(sua)
        #             #sua.save(activity=activity)
        #             #else:
        #                 #return False
        #         #print(1)
        #         self.url=""
        #         return True


class Application_tab_View(BaseView, NavMixin):
    def get_template_names(self):#获取template_name
        if self.request.user.is_staff:
            return ['sua/admin/admin_applications.html']
        elif self.request.user.student.power == 1:
            return ['sua/student_manager/manager_applications.html']
        else:
            return ['sua/student/applications.html']
    # template_name = 'sua/student/applications.html'
    components = {
        'nav': 'nav',
    }


    def serialize(self, request, *args, **kwargs):
        serialized = super(Application_tab_View, self).serialize(request)

        user = request.user

        if user.is_staff:
            application_set = Application.objects.filter(deleted_at=None, is_checked=True).order_by('is_checked', '-created')# 获取所有已审核的申请,按时间的倒序排序
            unreviewed_applications_set = Application.objects.filter(deleted_at=None, is_checked=False).order_by('-created')#获取所有未审核的申请
            unreviewed_applications_data = ApplicationSerializer(
                unreviewed_applications_set,
                many=True,
                context={'request': request}
            )
            unreviewed_applications = unreviewed_applications_data.data
            for application in unreviewed_applications:
                application['created'] = tools.DateTime2String_SHOW(
                    tools.TZString2DateTime(application['created']))
            serialized.update({
                'unreviewed_applications': unreviewed_applications,
            })

        elif user.student.power == 1:
            my_applications_set = user.applications.filter(deleted_at=None).order_by('-created')#获取活动级管理员的申请
            application_set = Application.objects.filter(
            sua__activity__owner=user,
            sua__activity__is_created_by_student=False,
            deleted_at=None).order_by('-created')# 获取该活动管理员创建的活动的申请
            unreviewed_applications_set = Application.objects.filter(
            sua__activity__owner=user,
            sua__activity__is_created_by_student=False,
            deleted_at=None,
            is_checked=False,).order_by('-created')#获取所有未审核的申请

            my_applications_data = ApplicationSerializer(
                my_applications_set,
                many=True,
                context={'request':request},
            )
            unreviewed_applications_data = ApplicationSerializer(
                unreviewed_applications_set,
                many=True,
                context={'request': request},
            )

            my_applications = my_applications_data.data
            unreviewed_applications = unreviewed_applications_data.data

            for application in unreviewed_applications:
                application['created'] = tools.DateTime2String_SHOW(
                    tools.TZString2DateTime(application['created']))
            for application in my_applications:
                application['created'] = tools.DateTime2String_SHOW(
                    tools.TZString2DateTime(application['created']))
            serialized.update({
                'unreviewed_applications': unreviewed_applications,
                'my_applications':my_applications,
            })
        else:
            application_set = user.applications.filter(
            deleted_at=None).order_by('-created')# 获取该学生创建的活动的申请

        application_data = ApplicationSerializer(  # 序列化所有申请
            application_set,
            many=True,
            context={'request': request}
        )

        applications = application_data.data

        for application in applications:
            application['created'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(application['created']))



        serialized.update({
            'applications': applications,
        })

        return serialized


class Appeal_tab_View(BaseView, NavMixin):
    def get_template_names(self):#获取template_name
        if self.request.user.is_staff:
            return ['sua/admin/admin_appeals.html']
        elif self.request.user.student.power == 1:
            return ['sua/student_manager/manager_appeals.html']
        else:
            return ['sua/student/appeals.html']
    # template_name = 'sua/student/appeals.html'
    components = {
        'nav': 'nav',
    }


    def serialize(self, request, *args, **kwargs):
        serialized = super(Appeal_tab_View, self).serialize(request)

        user = request.user

        if user.is_staff:
            appeal_set = Appeal.objects.filter(deleted_at=None, is_checked=True).order_by(
                'is_checked', '-created')  # 获取所有已审核的申诉
            unreviewed_appeals_set = Appeal.objects.filter(deleted_at=None, is_checked=False).order_by('-created')#获取未审核的申诉
            unreviewed_appeals_data = AppealSerializer(
                unreviewed_appeals_set,
                many=True,
                context={'request':request},
            )
            unreviewed_appeals = unreviewed_appeals_data.data
            for appeal in unreviewed_appeals:
                appeal['created'] = tools.DateTime2String_SHOW(
                    tools.TZString2DateTime(appeal['created']))
            serialized.update({
                'unreviewed_appeals':unreviewed_appeals,
            })
        elif user.student.power == 1:
            my_appeal_set = user.appeals.filter(deleted_at=None).order_by('-created')#获取活动管理员的申诉
            appeal_set = Appeal.objects.filter(
                publicity__activity__owner=user,
                publicity__activity__is_created_by_student=False,
                deleted_at=None,
                is_checked=True).order_by('is_checked', '-created')  # 获取所有已审核的申诉
            unreviewed_appeals_set = Appeal.objects.filter(
                publicity__activity__owner=user,
                publicity__activity__is_created_by_student=False,
                deleted_at=None,
                is_checked=False).order_by('-created')#获取未审核的申诉

            my_appeals_data = AppealSerializer(
                my_appeal_set,
                many=True,
                context={'request':request},
            )
            my_appeals = my_appeals_data.data

            unreviewed_appeals_data = AppealSerializer(
                unreviewed_appeals_set,
                many=True,
                context={'request':request},
            )
            unreviewed_appeals = unreviewed_appeals_data.data

            for appeal in unreviewed_appeals:
                appeal['created'] = tools.DateTime2String_SHOW(
                    tools.TZString2DateTime(appeal['created']))
            for appeal in my_appeals:
                appeal['created'] = tools.DateTime2String_SHOW(
                    tools.TZString2DateTime(appeal['created']))
            serialized.update({
                'unreviewed_appeals':unreviewed_appeals,
                'my_appeals':my_appeals,
            })



        elif hasattr(user,'student'):
            appeal_set = user.appeals.filter(deleted_at=None).order_by('-created')#获取该学生创建的申诉


        appeal_data = AppealSerializer(  # 序列化申诉
            appeal_set,
            many=True,
            context={'request': request}
        )

        appeals = appeal_data.data


        for appeal in appeals:
            appeal['created'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(appeal['created']))


        serialized.update({
            'appeals': appeals,
        })

        return serialized

class Activity_tab_View(BaseView, NavMixin):
    def get_template_names(self):#获取模版页面
        if self.request.user.is_staff:
            return ['sua/admin/admin_activities.html']
        elif self.request.user.student.power == 1:
            return ['sua/student_manager/manager_activities.html']
    #template_name = 'sua/admin/admin_activities.html'
    components = {
        'nav': 'nav',
    }


    def serialize(self, request, *args, **kwargs):
        serialized = super(Activity_tab_View, self).serialize(request)

        user = request.user

        if user.is_staff:
            activity_set = Activity.objects.filter(deleted_at=None).order_by('-created')  # 获取所有活动
        elif user.student.power == 1:
            activity_set = Activity.objects.filter(
                owner = user,
                deleted_at = None,
                is_created_by_student=False,
            ).order_by('-created')#获取管理员创建的活动

        activity_data = ActivitySerializer(  # 序列化申诉
            activity_set,
            many=True,
            context={'request': request}
        )
        activities = activity_data.data
        for i in range(len(activities)):
            activities[i]['number'] = activity_set[i].number()
            activities[i]['is_published'] = activity_set[i].get_is_published()#获取活动是否公示，若是，则将数据序列化
            if activities[i]['is_published']:
                publicity_data = PublicitySerializer(
                    activities[i]['is_published'],
                    many=True,
                    context={'request':request},
                )
                publicity = publicity_data.data
                activities[i]['is_published'] = publicity[0]['url']

        serialized.update({
            'activities': activities,
        })

        return serialized


class Student_tab_View(BaseView, NavMixin):

    template_name = 'sua/admin/admin_students.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        serialized = super(Student_tab_View, self).serialize(request)
        user = request.user

        if user.is_staff:
            classtypes =set([])
            grades =set([])
            student_all = Student.objects.filter(deleted_at=None,).order_by('number') #获取所有学生
            for student in student_all:
                classtypes.add(student.classtype)
                grades.add(student.grade)

            if 'classtype' and 'grade' in request.GET:
                classtype = request.GET.get('classtype')
                grade = request.GET.get('grade')
                student_set = Student.objects.filter(deleted_at=None,classtype=classtype,grade=grade).order_by('number')
            else:
                student_set = Student.objects.filter(deleted_at=None,).order_by('number')  # 获取筛选的学生

            student_data = StudentSerializer(  # 序列化所有学生信息
                student_set,
                many=True,
                context={'request': request}
            )
            serialized.update({
                'students': student_data.data,
                'classtypes':classtypes,
                'grades':grades,
            })
        return serialized


class Deleted_tab_View(BaseView, NavMixin):
    def get_template_names(self):
        if self.request.user.is_staff:
            return ['sua/admin/admin_deletes.html']
        elif self.request.user.student.power == 1:
            return ['sua/student_manager/manager_deletes.html']
    #template_name = 'sua/admin/admin_deletes.html'
    components = {
        'nav': 'nav',
    }
    def serialize(self, request, *args, **kwargs):
        serialized = super(Deleted_tab_View, self).serialize(request)

        user = request.user
        deleteds = {}

        if user.is_staff or user.student.power == 1:
            if user.is_staff:
                deleteds['students'] = tools.get_deleteds(Student, StudentSerializer, request)
                deleteds['applications'] = tools.get_deleteds(Application, ApplicationSerializer, request)
                # deleteds['activities'] = tools.get_deleteds(Activity, ActivitySerializer, request)
                deleteds['appeals'] = tools.get_deleteds(Appeal, AppealSerializer, request)

                activity_set = Activity.objects.order_by('-deleted_at').exclude(deleted_at=None) #获取被删除的活动
            else:
                activity_set = Activity.objects.filter(
                    deleted_by = user.student,
                ).order_by('-deleted_at').exclude(deleted_at=None)#获取管理员删除的活动

            activity_data = ActivitySerializer(
                activity_set,
                many = True,
                context={'request':request}
            )
            activities = activity_data.data
            for i in range(len(activity_set)):
                activities[i]['number'] = activity_set[i].number()
                activities[i]['deleted_at'] = tools.DateTime2String_SHOW(activity_set[i].deleted_at)
            deleteds['activities'] = activities

            if hasattr(user,'student'):
                if user.student.power == 1:
                    application_set = Application.objects.filter(
                    deleted_by=user,).order_by('-deleted_at').exclude(deleted_at=None)# 获取该活动管理员删除的活动的申请
                    application_data = ApplicationSerializer(  # 序列化所有申请
                        application_set,
                        many=True,
                        context={'request': request}
                    )

                    applications = application_data.data
                    deleteds['applications'] = applications

                    appeal_set = Appeal.objects.filter(
                    deleted_by=user,).order_by('-deleted_at').exclude(deleted_at=None)# 获取该活动管理员删除的活动的申诉
                    appeal_data = AppealSerializer(  # 序列化所有申请
                        appeal_set,
                        many=True,
                        context={'request': request}
                    )

                    appeals = appeal_data.data
                    deleteds['appeals'] = appeals


        for application in deleteds['applications']:
            application['created'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(application['created']))
        for appeal in deleteds['appeals']:
            appeal['created'] = tools.DateTime2String_SHOW(
                tools.TZString2DateTime(appeal['created']))
        serialized.update({
            'deleteds': deleteds,
        })
        return serialized
