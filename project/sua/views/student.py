from django.utils import timezone

from project.sua.serializers import PublicitySerializer, SuaSerializer, ApplicationSerializer
from project.sua.serializers import ApplicationSerializer, AppealSerializer
from project.sua.models import Publicity, Sua, Application
from project.sua.views.base import BaseView
from project.sua.views.mixins import NavMixin


class IndexView(BaseView, NavMixin):
    template_name = 'sua/index.html'
    components = {
        'nav': 'nav',
    }

    def do_serializations(self, request):
        serializeds = super(IndexView, self).do_serializations(request)

        user = request.user

        publicities = Publicity.objects.filter(  # 获取在公示期内的所有公示
            is_published=True,
            begin__lte=timezone.now(),
            end__gte=timezone.now()
        )
        publicitySerializer = PublicitySerializer(  # 序列化公示
            publicities,
            many=True,
            context={'request': request}
        )

        applicationSerializer = ApplicationSerializer(  # 序列化当前用户的所有申请
            user.applications,
            many=True,
            context={'request': request}
        )

        serializeds.update({
            'publicities': publicitySerializer.data,
            'applications': applicationSerializer.data
        })

        if hasattr(user, 'student'):  # 判断当前用户是否为学生
            student = user.student

            suaSerializer = SuaSerializer(  # 序列化当前学生的所有公益时记录
                student.suas,
                many=True,
                context={'request': request}
            )

            appealSerializer = AppealSerializer(  # 序列化当前学生的所有申诉
                student.appeals,
                many=True,
                context={'request': request}
            )

            serializeds.update({
                'suas': suaSerializer.data,
                'appeals': appealSerializer.data
            })

        return serializeds
