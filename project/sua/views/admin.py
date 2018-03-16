from django.utils import timezone
from django.http import HttpResponse


from project.sua.models import Publicity
from project.sua.models import Sua
from project.sua.models import Application
from project.sua.models import Student
from project.sua.models import Activity
from project.sua.models import Appeal


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
