import os

from django.utils import timezone
from django.http import HttpResponse


from project.sua.models import Publicity

from project.sua.serializers import PublicitySerializer
from project.sua.serializers import SuaSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import AppealSerializer
from project.sua.serializers import AddAppealSerializer
from project.sua.serializers import DEAddApplicationsSerializer, DEActivityForAddApplicationsSerializer, DESuaForAddApplicationsSerializer, DEProofForAddApplicationsSerializer

from .utils.base import BaseView
from .utils.mixins import NavMixin

from .forms.serializers import AddStudentSerializer,AddPublicitySerializer

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

class IndexView(BaseView, NavMixin):
    template_name = 'sua/index.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        serialized = super(IndexView, self).serialize(request)

        user = request.user

        publicity_set = Publicity.objects.filter(  # 获取在公示期内的所有公示
            is_published=True,
            begin__lte=timezone.now(),
            end__gte=timezone.now()
        )
        publicity_data = PublicitySerializer(  # 序列化公示
            publicity_set,
            many=True,
            context={'request': request}
        )

        application_data = ApplicationSerializer(  # 序列化当前用户的所有申请
            user.applications,
            many=True,
            context={'request': request}
        )

        serialized.update({
            'publicities': publicity_data.data,
            'applications': application_data.data
        })

        if hasattr(user, 'student'):  # 判断当前用户是否为学生
            student = user.student

            sua_data = SuaSerializer(  # 序列化当前学生的所有公益时记录
                student.suas.filter(is_valid=True),
                many=True,
                context={'request': request}
            )

            appeal_data = AppealSerializer(  # 序列化当前学生的所有申诉
                student.appeals,
                many=True,
                context={'request': request}
            )

            serialized.update({
                'suas': sua_data.data,
                'appeals': appeal_data.data
            })

        return serialized


class TestBaseView(BaseView, NavMixin):  # 例子：这是一个创建学生的View（怕你们踩坑了）
    template_name = 'sua/tmp/test.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        serialized = super(TestBaseView, self).serialize(request)
        serializer = AddStudentSerializer()
        serialized.update({
            'serializer': serializer,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        serializer = AddStudentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            self.url = serializer.data['url']
            return True
        else:
            return False


class AppealView(BaseView,NavMixin):
    template_name = 'sua/appeal.html'
    components = {
        'nav': 'nav',
    }

    def serialize(self, request, *args, **kwargs):
        publicity_id = kwargs['pk']
        publicity = AddPublicitySerializer(Publicity.objects.get(id=publicity_id),context={'request':request})
        serialized = super(AppealView, self).serialize(request)
        serializer = AddAppealSerializer(context={'request':request})
        serialized.update({
            'serializer': serializer,
            'publicity':publicity.data,
        })
        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        assert hasattr(user,'student') # 判断当前用户是否为学生
        student = user.student

        publicity_id = kwargs['pk']
        serializer = AddAppealSerializer(data=request.data, context={'request': request,})
        if serializer.is_valid():

            serializer.save(publicity=Publicity.objects.get(id=publicity_id),owner=user,student=student)
            self.url = serializer.data['url']
            return True
        else:
            return False


class SuasExportView(BaseView,NavMixin):
    template_name = 'sua/suas_export.html'
    components = {
        'nav': 'nav',
    }


    def serialize(self, request, *args, **kwargs):
        serialized = super(SuasExportView, self).serialize(request)

        user = request.user

        if hasattr(user, 'student'):  # 判断当前用户是否为学生
            student = user.student

            sua_data = SuaSerializer(# 序列化当前学生的所有公益时记录
                student.suas.filter(is_valid=True),
                many=True,
                context={'request': request}
            )

        serialized.update({
            'suas': sua_data.data,
            'name':student.name,
            'number':student.number,
            'hours':student.suahours,
            })


        return serialized


def Download(request):

    pdfmetrics.registerFont(TTFont('song', os.getcwd() + '/project/sua/views/STSONG.ttf'))
    user = request.user

    student = user.student
    Filename = 'str(student.name)'

    sua_data = SuaSerializer(# 序列化当前学生的所有公益时记录
        student.suas.filter(is_valid=True),
        many=True,
        context={'request': request}
    )


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=公益时'

    buffer = BytesIO()
    zuo = 50
    kuan = 210
    you = 545
    p = canvas.Canvas(buffer)

    p.filename = student.name

    p.setFont("song", 22)#字号
    p.drawString(zuo-5,780,"公益时记录",)#标题
    p.drawImage('project/sua/static/sua/images/logo-icon.png',460,705,width=90,height=90)#学院标志
    p.setFont("song", 15) #字号
    p.drawString(zuo-5,750,'学号:'+str(user))#学号
    p.drawString(zuo+150,750,'名字:'+str(student.name))#名字
    p.drawString(zuo-5,720,'总公益时数:'+str(student.suahours)+'h')#总公益时

    location = 640
    p.drawString(zuo,680,"活动名称")
    p.drawString(zuo+kuan,680,"活动团体")
    p.drawString(zuo+kuan*2,680,"公益时数")
    for sua in sua_data.data:
        p.drawString(zuo,location,str(sua['activity']['title']))#活动主题
        p.drawString(zuo+kuan,location,str(sua['activity']['group']))#活动团体
        p.drawString(zuo+kuan*2,location,str(sua['suahours'])+'h')#公益时数
        location -= 50
        p.line(zuo-5,location+15,you,location+15)#第N横


    p.line(zuo-5,700,you,700)#第一横
    p.line(zuo-5,655,you,655)#第二横
    p.line(zuo-5,700,zuo-5,location+15)#第一丨
    p.line(you,700,you,location+15)#第四丨
    p.line(zuo+kuan-5,700,zuo+kuan-5,location+15)#第二丨
    p.line(zuo+2*kuan-5,700,zuo+2*kuan-5,location+15)#第三丨


    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


class ApplyView(BaseView, NavMixin):
    template_name = 'sua/apply_sua.html'
    components = {
        'nav': 'nav',
    }


    def serialize(self, request, *args, **kwargs):
        serialized = super(ApplyView, self).serialize(request)

        user = request.user
        if hasattr(user, 'student'): # 判断当前用户是否为学生
            activity_serializer = DEActivityForAddApplicationsSerializer()
            sua_serializer = DESuaForAddApplicationsSerializer()
            proof_serializer = DEProofForAddApplicationsSerializer()
            application_serializer = DEAddApplicationsSerializer()

            serialized.update({
                'activities':activity_serializer,
                'suas':sua_serializer,
                'proofs':proof_serializer,
                'applications':application_serializer
            })

        return serialized

    def deserialize(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'student'):  # 判断当前用户是否为学生
            student = user.student

        else:
            return False

        activity_serializer = DEActivityForAddApplicationsSerializer(data=request.data, context={'request': request})
        sua_serializer = DESuaForAddApplicationsSerializer(data=request.data, context={'request': request})
        proof_serializer = DEProofForAddApplicationsSerializer(data=request.data, context={'request': request})
        application_serializer = DEAddApplicationsSerializer(data=request.data, context={'request': request})
        if activity_serializer.is_valid() and sua_serializer.is_valid() and application_serializer.is_valid() and proof_serializer.is_valid():

            activity = activity_serializer.save(owner=user)
            sua = sua_serializer.save(activity=activity, owner=user, student=student)
            proof = proof_serializer.save(owner=user)
            application_serializer.save(sua=sua, proof=proof, owner=user)
            self.url = application_serializer.data['url']
            return True
        else:
            return False
