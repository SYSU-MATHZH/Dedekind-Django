from django.urls import path, include
from django.contrib.auth.decorators import login_required
from project.sua.views import api, auth, student ,admin

from rest_framework import routers
from django.conf.urls import url


router = routers.DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'groups', api.GroupViewSet)
router.register(r'students', api.StudentViewSet)
router.register(r'suagroups', api.SuaGroupViewSet)
router.register(r'suas', api.SuaViewSet)
router.register(r'activities', api.ActivityViewSet)
router.register(r'applications', api.ApplicationViewSet)
router.register(r'publicities', api.PublicityViewSet)
router.register(r'appeals', api.AppealViewSet)
router.register(r'proofs', api.ProofViewSet)

#
#
#app_name = 'sua'
urlpatterns = [
    path('suas/export/',login_required(student.SuasExportView.as_view())),
    path('', login_required(student.IndexView.as_view()), name='index'),
    path('', include(router.urls)),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('test/', login_required(student.TestBaseView.as_view())),
    path('publicities/<int:pk>/appeal/', login_required(student.AppealView.as_view())),
    path('suas/export/download/',login_required(student.Download)),
    path('admin/',login_required(admin.IndexView.as_view())),
    path('admin/appeals/<int:pk>/change/',login_required(admin.AppealView.as_view())),
#     path('playMFS/', views.playMFS, name='playMFS'),
#     path('admin/', views.adminIndex, name='admin-index'),
#     path('apply_sua/', views.apply_sua, name='apply_sua'),
#     path('appeal_for/', views.appeal_for, name='appeal_for'),
#     path(
#         'student/list/',
#         views.JSONStudentListView.as_view(),
#         name='student-list-json',
#     ),
#     path(
#         'student/<int:pk>/sualist/',
#         views.JSONStudentSuaListView.as_view(),
#         name='student-sualist-json',
#     ),
#     path(
#         'student/<int:pk>/grouplist/',
#         login_required(views.JSONStudentGroupListView.as_view()),
#         name='student-grouplist-json',
#     ),
#     path(
#         'sua/<int:pk>/application/',
#         login_required(views.JSONSuaApplicationView.as_view()),
#         name='sua-application-json',
#     ),
#     path(
#         'sua/<int:pk>/gsua/',
#         login_required(views.JSONSuaGSuaListView.as_view()),
#         name='sua-gsua-json',
#     ),
#     path(
#         'application/checklist/',
#         login_required(views.JSONApplicationCheckListView.as_view()),
#         name='application-checklist-json',
#     ),
#     path(
#         'gsuap/list/',
#         login_required(views.JSONGSuaPublicityListView.as_view()),
#         name='gsuap-list-json',
#     ),
#     path(
#         'gsua/<int:pk>/sualist/',
#         login_required(views.JSONGSuaSuaListView.as_view()),
#         name='gsua-sualist-json',
#     ),
#     path(
#         'suagroup/<int:pk>/appeallist/',
#         login_required(views.JSONSuaGroupAppealListView.as_view()),
#         name='suagroup-appeallist-json',
#     ),
#     path(
#         'suagroup/list/',
#         login_required(views.JSONSuaGroupListView.as_view()),
#         name='suagroup-list-json',
#     ),
#     path(
#         'student/<int:pk>/',
#         login_required(views.StudentDetailView.as_view()),
#         name='student-detail',
#     ),
#     path(
#         'student/add/',
#         login_required(views.StudentCreate.as_view()),
#         name='student-add',
#     ),
#     path(
#         'student/<int:pk>/update/',
#         login_required(views.StudentUpdate.as_view()),
#         name='student-update',
#     ),
#     path(
#         'student/<int:pk>/delete/',
#         login_required(views.StudentDelete.as_view()),
#         name='student-delete',
#     ),
#     path(
#         'application/<int:pk>/',
#         login_required(views.Sua_ApplicationDetailView.as_view()),
#         name='application-detail',
#     ),
#     path(
#         'application/student/<int:pk>/add/',
#         login_required(views.Sua_ApplicationCreate.as_view()),
#         name='application-add',
#     ),
#     path(
#         'application/<int:pk>/update/',
#         login_required(views.Sua_ApplicationUpdate.as_view()),
#         name='application-update',
#     ),
#     path(
#         'application/<int:pk>/delete/',
#         login_required(views.Sua_ApplicationDelete.as_view()),
#         name='application-delete',
#     ),
#     path(
#         'application/<int:pk>/check/',
#         login_required(views.Sua_ApplicationCheck.as_view()),
#         name='application-check',
#     ),
#     path(
#         'gsuap/<int:pk>/',
#         login_required(views.GSuaPublicityDetailView.as_view()),
#         name='gsuap-detail',
#     ),
#     path(
#         'gsuap/add/',
#         login_required(views.GSuaPublicityCreate.as_view()),
#         name='gsuap-add',
#     ),
#     path(
#         'gsuap/<int:pk>/update/',
#         login_required(views.GSuaPublicityUpdate.as_view()),
#         name='gsuap-update',
#     ),
#     path(
#         'gsua/<int:pk>/delete/',
#         login_required(views.GSuaDelete.as_view()),
#         name='gsua-delete',
#     ),
#     path(
#         'appeal/<int:pk>/',
#         login_required(views.AppealDetailView.as_view()),
#         name='appeal-detail',
#     ),
#     path(
#         'appeal/<int:pk>/update/',
#         login_required(views.AppealUpdate.as_view()),
#         name='appeal-update',
#     ),
#     path(
#         'appeal/<int:pk>/check/',
#         login_required(views.AppealCheck.as_view()),
#         name='appeal-check',
#     ),
#
]
