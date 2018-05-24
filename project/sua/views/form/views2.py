from .base import BaseViewSet

from rest_framework.permissions import IsAdminUser
from project.sua.views.utils.mixins import NavMixin
from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly,IsAdminUserOrActivity
from project.sua.models import Student,Activity,Application
import project.sua.views.form.serializers as firs
import project.sua.serializers as sirs


class StudentViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddStudentSerializer
    queryset = Student.objects.filter(deletedAt=None)
    revoke_queryset = Student.objects.all()
    revoke_success_url = delete_success_url = '/admin/'
    # filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/student_form.html']
        elif self.action == 'detail':
            return ['sua/student_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change']:
            return firs.AddStudentSerializer
        elif self.action == 'detail':
            return firs.detailofstudentSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['add', 'change']:
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUser, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]


class ActivityViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = sirs.ActivitySerializer
    queryset = Activity.objects.filter(deletedAt=None)
    revoke_queryset = Activity.objects.all()
    revoke_success_url = delete_success_url = '/admin/'

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/activity_form.html']
        elif self.action == 'detail':
            return ['sua/activity_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change']:
            return firs.AddActivitySerializer
        elif self.action == 'detail':
            return firs.AddActivitySerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['add', 'change']:
            permission_classes = (IsAdminUserOrActivity, )
        elif self.action == 'detail':
            permission_classes = (IsAdminUserOrActivity, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)


class ApplicationViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = sirs.ApplicationSerializer
    queryset = Application.objects.filter(deletedAt=None)
    # filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/application_form.html']
        elif self.action == 'detail':
            return ['sua/application_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change']:
            return firs.AddApplicationSerializer
        elif self.action == 'detail':
            return firs.AddApplicationSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['change']:
            permission_classes = (IsAdminUser,  )
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUser, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
