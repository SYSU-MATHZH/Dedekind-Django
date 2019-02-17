<<<<<<< HEAD
from django.urls import path, include
from django.contrib.auth.decorators import login_required
import project.sua.views.auth.views as auth
import project.sua.views.admin.views as admin
import project.sua.views.student.views as student
import project.sua.views.form.views as form
import project.sua.views.form.views2 as form2
from project.sua.views.form.base import StudentViewSet
from project.sua.views.apis import apis, auths
from project.sua.views.index.views import IndexView, Application_tab_View, Appeal_tab_View, Activity_tab_View, Student_tab_View, Deleted_tab_View

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', form.UserViewSet)
router.register(r'groups', form.GroupViewSet)
router.register(r'students', form2.StudentViewSet)
router.register(r'suagroups', form.SuaGroupViewSet)
router.register(r'suas', form2.SuaViewSet)
router.register(r'activities', form2.ActivityViewSet)
router.register(r'applications', form2.ApplicationViewSet)
router.register(r'publicities', form2.PublicityViewSet)
router.register(r'appeals', form2.AppealViewSet)
router.register(r'proofs', form2.ProofViewSet)
router.register(r'base', StudentViewSet, base_name='base')

rou = routers.DefaultRouter()
rou.register(r'users', apis.UserViewSet,base_name = "api-user")
rou.register(r'students', apis.StudentViewSet, base_name="api-student")
rou.register(r'activities', apis.ActivityViewSet, base_name="api-activity")
rou.register(r'publicities', apis.PublicityViewSet, base_name="api-publicity")
rou.register(r'proofs', apis.ProofViewSet, base_name="api-proof")
rou.register(r'applications', apis.ApplicationViewSet, base_name="api-application")
rou.register(r'suas', apis.SuaViewSet, base_name="api-sua")
rou.register(r'appeals', apis.AppealViewSet, base_name="api-appeal")


# app_name = 'sua'
urlpatterns = [
    path('',login_required(IndexView.as_view()), name='index'),
    path('suas/export/',login_required(student.SuasExportView.as_view())),
#    path('', login_required(student.IndexView.as_view()), name='index'),
    path('apis/',include(rou.urls)),
    path('', include(router.urls)),
    path('apis/login/', auths.LoginView.as_view()),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),

    path('publicities/<int:pk>/appeal/', login_required(student.AppealView.as_view())),
    path('applications/apply/', login_required(student.ApplyView.as_view())),
    path('suas/export/download/',login_required(student.Download)),
#    path('admin/',login_required(admin.IndexView.as_view())),
    path('admin/appeals/<int:pk>/change/',login_required(admin.AppealView.as_view())),
    path('admin/applications/<int:pk>/change/',login_required(admin.ApplicationView.as_view())),
    path('admin/publicities/<int:pk>/create/',login_required(admin.PublicityView.as_view())),
    path('admin/publicities/<int:pk>/change/',login_required(admin.ChangePublicityView.as_view())),
    path('admin/publicities/<int:pk>/manage/',login_required(admin.ManagePublicityView.as_view())),
    path('admin/activities/<int:pk>/suas/add/',login_required(admin.AddSuaForActivityView.as_view())),
    path('admin/suas/<int:pk>/change/',login_required(admin.ChangeSuaForActivityView.as_view())),
    path('applications/merge',login_required(admin.ApplicationsMergeView.as_view())),
    path('admin/activities/<int:pk>/check/',login_required(admin.CheckTheActivityView)),
    path('admin/publicities/<int:pk>/check/',login_required(admin.CheckThePublicityView)),
    path('admin/applications/<int:pk>/mark/', login_required(admin.MarkApplicationView)),
    path('admin/suas/<int:pk>/check/',login_required(admin.CheckTheSuaView)),
    path('students/<int:pk>/changepassword/',login_required(student.ChangePasswordView.as_view())),
    path('admin/activities/<int:pk>/batch_suas/add/',login_required(admin.Batch_AddSuasView.as_view())),

    path('applications/tab',login_required(Application_tab_View.as_view()), ),
    path('appeals/tab',login_required(Appeal_tab_View.as_view()), ),
    path('students/tab',login_required(Student_tab_View.as_view()), ),
    path('activities/tab',login_required(Activity_tab_View.as_view()), ),
    path('deleteds/tab',login_required(Deleted_tab_View.as_view()), ),
]
=======
from django.urls import path, include
from django.contrib.auth.decorators import login_required
import project.sua.views.auth.views as auth
import project.sua.views.admin.views as admin
import project.sua.views.student.views as student
import project.sua.views.form.views as form
import project.sua.views.form.views2 as form2
from project.sua.views.form.base import StudentViewSet
from project.sua.views.apis import apis, auths
from project.sua.views.index.views import IndexView, Application_tab_View, Appeal_tab_View, Activity_tab_View, Student_tab_View, Deleted_tab_View

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', form.UserViewSet)
router.register(r'groups', form.GroupViewSet)
router.register(r'students', form2.StudentViewSet)
router.register(r'suagroups', form.SuaGroupViewSet)
router.register(r'suas', form2.SuaViewSet)
router.register(r'activities', form2.ActivityViewSet)
router.register(r'applications', form2.ApplicationViewSet)
router.register(r'publicities', form2.PublicityViewSet)
router.register(r'appeals', form2.AppealViewSet)
router.register(r'proofs', form2.ProofViewSet)
router.register(r'base', StudentViewSet, base_name='base')

rou = routers.DefaultRouter()
rou.register(r'users', apis.UserViewSet,base_name = "api-user")
rou.register(r'students', apis.StudentViewSet, base_name="api-student")
rou.register(r'activities', apis.ActivityViewSet, base_name="api-activity")
rou.register(r'publicities', apis.PublicityViewSet, base_name="api-publicity")
rou.register(r'proofs', apis.ProofViewSet, base_name="api-proof")
rou.register(r'applications', apis.ApplicationViewSet, base_name="api-application")
rou.register(r'suas', apis.SuaViewSet, base_name="api-sua")
rou.register(r'appeals', apis.AppealViewSet, base_name="api-appeal")


# app_name = 'sua'
urlpatterns = [
    path('',login_required(IndexView.as_view()), name='index'),
    path('suas/export/',login_required(student.SuasExportView.as_view())),
#    path('', login_required(student.IndexView.as_view()), name='index'),
    path('apis/',include(rou.urls)),
    path('', include(router.urls)),
    path('apis/login/', auths.LoginView.as_view()),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),

    path('publicities/<int:pk>/appeal/', login_required(student.AppealView.as_view())),
    path('applications/apply/', login_required(student.ApplyView.as_view())),
    path('suas/export/download/',login_required(student.Download)),
#    path('admin/',login_required(admin.IndexView.as_view())),
    path('admin/appeals/<int:pk>/change/',login_required(admin.AppealView.as_view())),
    path('admin/applications/<int:pk>/change/',login_required(admin.ApplicationView.as_view())),
    path('admin/publicities/<int:pk>/create/',login_required(admin.PublicityView.as_view())),
    path('admin/publicities/<int:pk>/change/',login_required(admin.ChangePublicityView.as_view())),
    path('admin/publicities/<int:pk>/manage/',login_required(admin.ManagePublicityView.as_view())),
    path('admin/activities/<int:pk>/suas/add/',login_required(admin.AddSuaForActivityView.as_view())),
    path('admin/suas/<int:pk>/change/',login_required(admin.ChangeSuaForActivityView.as_view())),
    path('applications/merge',login_required(admin.ApplicationsMergeView.as_view())),
    path('admin/activities/<int:pk>/check/',login_required(admin.CheckTheActivityView)),
    path('admin/publicities/<int:pk>/check/',login_required(admin.CheckThePublicityView)),
    path('admin/suas/<int:pk>/check/',login_required(admin.CheckTheSuaView)),
    path('students/<int:pk>/changepassword/',login_required(student.ChangePasswordView.as_view())),
    path('admin/activities/<int:pk>/batch_suas/add/',login_required(admin.Batch_AddSuasView.as_view())),

    path('applications/tab',login_required(Application_tab_View.as_view()), ),
    path('appeals/tab',login_required(Appeal_tab_View.as_view()), ),
    path('students/tab',login_required(Student_tab_View.as_view()), ),
    path('activities/tab',login_required(Activity_tab_View.as_view()), ),
    path('deleteds/tab',login_required(Deleted_tab_View.as_view()), ),
    path('admin/AcademicYear/',login_required(admin.AcademicYearView.as_view()), ),
    path('activities/<int:pk>/download/', login_required(admin.ActivityDownload) )
]
>>>>>>> 4aeedf022c269cdd7612b09a4c4b063cbcb5fdf6
