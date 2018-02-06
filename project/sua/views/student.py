from django.utils import timezone

from project.sua.models import Publicity
from project.sua.models import Sua
from project.sua.models import Application

from project.sua.serializers import PublicitySerializer
from project.sua.serializers import SuaSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import ApplicationSerializer
from project.sua.serializers import AppealSerializer

from .utils.base import BaseView
from .utils.mixins import NavMixin


class IndexView(BaseView, NavMixin):
    template_name = 'sua/index.html'
    components = {
        'nav': 'nav',
    }

    def do_serializations(self, request):
        serializeds = super(IndexView, self).do_serializations(request)

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

        serializeds.update({
            'publicities': publicity_data.data,
            'applications': application_data.data
        })

        if hasattr(user, 'student'):  # 判断当前用户是否为学生
            student = user.student

            sua_data = SuaSerializer(  # 序列化当前学生的所有公益时记录
                student.suas,
                many=True,
                context={'request': request}
            )

            appeal_data = AppealSerializer(  # 序列化当前学生的所有申诉
                student.appeals,
                many=True,
                context={'request': request}
            )

            serializeds.update({
                'suas': sua_data.data,
                'appeals': appeal_data.data
            })

        return serializeds
