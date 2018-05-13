from django.urls import path, include
from django.contrib.auth.decorators import login_required
import project.sua.views.auth.views as auth
import project.sua.views.admin.views as admin
import project.sua.views.student.views as student
import project.sua.views.form.views as form
from project.sua.views.apis import apis, auths

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', form.UserViewSet)
router.register(r'groups', form.GroupViewSet)
router.register(r'students', form.StudentViewSet)
router.register(r'suagroups', form.SuaGroupViewSet)
router.register(r'suas', form.SuaViewSet)
router.register(r'activities', form.ActivityViewSet)
router.register(r'applications', form.ApplicationViewSet)
router.register(r'publicities', form.PublicityViewSet)
router.register(r'appeals', form.AppealViewSet)
router.register(r'proofs', form.ProofViewSet)

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
    path('suas/export/',login_required(student.SuasExportView.as_view())),
    path('', login_required(student.IndexView.as_view()), name='index'),
    path('apis/',include(rou.urls)),
    path('', include(router.urls)),
    path('apis/login/', auths.LoginView.as_view()),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),

    path('publicities/<int:pk>/appeal/', login_required(student.AppealView.as_view())),
    path('applications/apply/', login_required(student.ApplyView.as_view())),
    path('suas/export/download/',login_required(student.Download)),
    path('admin/',login_required(admin.IndexView.as_view())),
    path('admin/appeals/<int:pk>/change/',login_required(admin.AppealView.as_view())),
    path('admin/applications/<int:pk>/change/',login_required(admin.ApplicationView.as_view())),
    path('admin/publicities/<int:pk>/create/',login_required(admin.PublicityView.as_view())),
    path('admin/publicities/<int:pk>/change/',login_required(admin.ChangePublicityView.as_view())),
    path('admin/publicities/<int:pk>/manage/',login_required(admin.ManagePublicityView.as_view())),
    path('admin/activities/<int:pk>/suas/add/',login_required(admin.AddSuaForActivityView.as_view())),
    path('admin/suas/<int:pk>/change/',login_required(admin.ChangeSuaForActivityView.as_view())),
    path('admin/activities/<int:pk>/check/',login_required(admin.CheckTheActivityView)),
]
