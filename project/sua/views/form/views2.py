from .base import BaseViewSet

from rest_framework.permissions import IsAdminUser
from project.sua.views.utils.mixins import NavMixin
from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly,IsAdminUserOrActivity,IsAdminUserOrStudent,IsTheStudentOrIsAdminUserOrActivityManager
from project.sua.models import Student, Sua, Activity, Application, Publicity, Appeal, Proof
import project.sua.views.form.serializers as firs
import project.sua.serializers as sirs

from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response


class StudentViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddStudentSerializer
    queryset = Student.objects.filter(deleted_at=None)
    revoke_queryset = Student.objects.all()
    revoke_success_url = '/deleteds/tab'
    delete_success_url = '/students/tab'

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
        if self.action in ['add','change']:
            permission_classes = (IsAdminUser, )
        elif self.action in ['detail',]:
            permission_classes = (IsAdminUserOrStudent, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]


class SuaViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }

    serializer_class = firs.AddSuaSerializer
    queryset = Sua.objects.filter(deleted_at=None)
    revoke_queryset = Sua.objects.all()
    revoke_success_url = delete_success_url = '/'

    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/sua_form.html']
        elif self.action == 'detail':
            return ['sua/sua_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddSuaSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes == (IsTheStudentOrIsAdminUser,)
        else:
            permission_classes = (IsAdminUserOrReadOnly,)

        return [permission() for permission in permission_classes]

    @detail_route(methods=['get'])
    def delete(self, request, *args, **kwargs):
        if 'from_url' in request.GET:
            self.delete_success_url = request.GET['from_url']
        instance = self.get_object()
        user = request.user
        deleted = None
        if user.is_staff or user.student.power == 1:
            if user.is_staff:
                deleted = user.username
            elif user.student.power == 1:
                deleted = user.student.name
        instance.deleted_by = deleted
        instance.save()
        self.perform_delete(instance)
        return self.get_delete_response()

class ActivityViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddActivitySerializer
    queryset = Activity.objects.filter(deleted_at=None)
    revoke_queryset = Activity.objects.all()
    revoke_success_url = '/deleteds/tab'
    delete_success_url = '/activities/tab'
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/activity_form.html']
        elif self.action == 'detail':
            return ['sua/activity_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddActivitySerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['add', 'change', 'detail']:
            permission_classes = (IsAdminUserOrActivity,)
        else:
            permission_classes = (IsAdminUserOrActivity, )

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save(owner=self.request.user, is_valid=True)
        elif self.request.user.student.power==1:
            serializer.save(owner=self.request.user, is_valid=False)


class ApplicationViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddApplicationSerializer
    queryset = Application.objects.filter(deleted_at=None)
    revoke_queryset = Application.objects.all()
    revoke_success_url = '/deleteds/tab'
    delete_success_url = '/applications/tab'
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/application_form.html']
        elif self.action == 'detail':
            return ['sua/application_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddApplicationSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUserOrActivityManager,)
        else:
            permission_classes = (IsAdminUserOrReadOnly,)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PublicityViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddPublicitySerializer
    queryset = Publicity.objects.filter(deleted_at=None)
    revoke_queryset = Publicity.objects.all()
    revoke_success_url = '/deleteds/tab'
    delete_success_url = '/'
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/publicity_form.html']
        elif self.action == 'detail':
            return ['sua/publicity_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddPublicitySerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser, )
        # elif self.action == 'detail':
        #     permission_classes = (IsTheStudentOrIsAdminUser,)
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]

class AppealViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddAppealSerializer
    queryset = Appeal.objects.filter(deleted_at=None)
    revoke_queryset = Appeal.objects.all()
    revoke_success_url = '/deleteds/tab'
    delete_success_url = '/appeals/tab'
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/appeal_form.html']
        elif self.action == 'detail':
            return ['sua/appeal_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddAppealSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser, )
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUserOrActivityManager, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]

class ProofViewSet(BaseViewSet, NavMixin):
    components = {
        'nav': 'nav',
    }
    serializer_class = firs.AddProofSerializer
    queryset = Proof.objects.filter(deleted_at=None)
    revoke_queryset = Proof.objects.all()
    revoke_success_url = delete_success_url = '/'
    #filter_fields = ('grade', 'classtype')

    def get_template_names(self):
        if self.action in ['add', 'change']:
            return ['sua/sua_form.html']
        elif self.action == 'detail':
            return ['sua/proof_detail.html']

    def get_serializer_class(self):
        if self.action in ['add', 'change', 'detail']:
            return firs.AddProofSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == 'change':
            permission_classes = (IsAdminUser,)
        elif self.action == 'detail':
            permission_classes = (IsTheStudentOrIsAdminUser, )
        else:
            permission_classes = (IsAdminUserOrReadOnly, )

        return [permission() for permission in permission_classes]
