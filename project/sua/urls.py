from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'suagroups', views.SuaGroupViewSet)
router.register(r'suas', views.SuaViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'applications', views.ApplicationViewSet)
router.register(r'publicities', views.PublicityViewSet)
router.register(r'appeals', views.AppealViewSet)
router.register(r'proofs', views.ProofViewSet)

#
#
app_name = 'sua'
urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
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
