from project.sua.serializers import UserSerializer, StudentSerializer
import project.sua.views.utils.tools as tools


class NavMixin(object):
    def nav(self, request, *args, **kwargs):
        navs = {}
        user = request.user
        student = None
        if hasattr(user, 'student'):
            student = user.student
        userSerializer = UserSerializer(user, context={'request': request})
        studentSerializer = StudentSerializer(student, context={'request': request})
        navs['user'] = userSerializer.data
        navs['student'] = studentSerializer.data
        navs['YEAR_CHOICES'] = tools.YEAR_CHOICES
        return navs
