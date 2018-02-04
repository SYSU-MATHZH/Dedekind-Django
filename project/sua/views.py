from django.views import generic
from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy, reverse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# from .forms import LoginForm, SuaForm, Sua_ApplicationForm, ProofForm, AppealForm, StudentForm, Sua_ApplicationCheckForm, GSuaPublicityForm, AppealCheckForm
from .api import check_signature
import json
import pprint

# 上面是旧Views的依赖

from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from project.sua.permissions import IsTheStudentOrIsAdminUser, IsAdminUserOrReadOnly



import project.sua.serializers as sirs
import project.sua.form.serializers as firs
import project.sua.form.mixins as mymixins

from .forms import LoginForm
from .models import Sua, Proof, Application, Publicity, Activity, Student, Appeal, SuaGroup
from django.contrib.auth.models import User, Group


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = sirs.UserSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = sirs.GroupSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class StudentViewSet(
        viewsets.ReadOnlyModelViewSet,
        mymixins.AddFormMixin,
        mymixins.ChangeFormMixin,
        mymixins.DetailFormMixin,
        mymixins.DeleteFormMixin
    ):
    """
    API endpoint that allows students to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = sirs.StudentSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_fields = ('grade', 'classtype')

    template_name = None  # 请务必要添加这一行，否则会报错

    delete_success_url = '/'

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/student_form.html',  # 模板文件
        add_serializer_class=firs.AddStudentSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
        permission_classes = (IsAdminUser, )
    )
    def add(self, request):
        '''
        url: api/students/add/
        template: sua/student_form.html
        GET: 向模板代码提供空Student序列化器(serializer)，渲染并返回Student创建表单
        POST: 接受Student创建表单数据，创建Student实例，并重定向至Student实例详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(StudentViewSet, self).add(request)

    @detail_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/student_form.html',  # 模板文件
        change_serializer_class=firs.AddStudentSerializer,  # 序列化器
        change_success_url='/',  # 成功后的跳转url
        permission_classes = (IsAdminUser, )
    )
    def change(self, request, *args, **kwargs):
        '''
        url: api/students/<int:pk>/change/
        template: sua/student_form.html
        GET: 向模板代码提供pk对应的student的序列化器(serializer)，渲染并返回Student更新表单
        POST: 接受Student更新表单数据，更新Student实例及对应的User实例，并重定向至Student实例详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(StudentViewSet, self).change(request, *args, **kwargs)

    @detail_route(
        methods=['get'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        permission_classes = (IsTheStudentOrIsAdminUser,),
        template_name='sua/student_detail.html',  # 模板文件
        detail_serializer_class=firs.AddStudentSerializer,  # 序列化器
    )
    def detail(self, request, *args, **kwargs):
        '''
        url: api/students/<int:pk>/detail/
        template: sua/student_detail.html
        GET: 向模板代码提供pk对应的student的序列化器(serializer)，渲染并返回Student详情页面
        表单字段：表单字段与serializer.data一致
        '''
        return super(StudentViewSet, self).detail(request, *args, **kwargs)


class SuaGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows suagroups to be viewed or edited.
    """
    queryset = SuaGroup.objects.all()
    serializer_class = sirs.SuaGroupSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class SuaViewSet(viewsets.ReadOnlyModelViewSet, mymixins.AddFormMixin):
    """
    API endpoint that allows suas to be viewed or edited.
    """
    queryset = Sua.objects.all()
    serializer_class = sirs.SuaSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/sua_form.html',  # 模板文件
        add_serializer_class=firs.AddSuaSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/suas/add/
        template: sua/sua_form.html
        GET: 返回空Sua序列化器，渲染Sua创建表单
        POST: 接受Sua创建表单数据，创建Sua实例，并重定向至对应的Activity详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(SuaViewSet, self).add(request)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class ActivityViewSet(viewsets.ReadOnlyModelViewSet, mymixins.AddFormMixin):
    """
    API endpoint that allows activities to be viewed or edited.
    """
    queryset = Activity.objects.all()
    serializer_class = sirs.ActivitySerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/activity_form.html',  # 模板文件
        add_serializer_class=firs.AddActivitySerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/activities/add/
        template: sua/activity_form.html
        GET: 返回空Activity序列化器，渲染Activity创建表单
        POST: 接受Activity创建表单数据，创建Activity实例，并重定向至对应的Activity详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(ActivityViewSet, self).add(request)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet, mymixins.AddFormMixin):
    """
    API endpoint that allows applications to be viewed or edited.
    """
    queryset = Application.objects.all()
    serializer_class = sirs.ApplicationSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/sua_form.html',  # 模板文件
        add_serializer_class=firs.AddApplicationSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/applications/add/
        template: sua/sua_form.html
        GET: 返回空Application序列化器，渲染Application创建表单
        POST: 接受Application创建表单数据，创建Application实例，并重定向至对应的Application详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(ApplicationViewSet, self).add(request)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class PublicityViewSet(viewsets.ReadOnlyModelViewSet,mymixins.AddFormMixin):
    """
    API endpoint that allows publicities to be viewed or edited.
    """
    queryset = Publicity.objects.all()
    serializer_class = sirs.PublicitySerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/gsua_publicity_form.html',  # 模板文件
        add_serializer_class=firs.AddPublicitySerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/publicities/add/
        template: sua/gsua_publicity_form.html
        GET: 返回空Publicity序列化器，渲染Publicity创建表单
        POST: 接受Publicity创建表单数据，创建Publicity实例，并重定向至对应的Publicity详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(PublicityViewSet, self).add(request)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class AppealViewSet(viewsets.ReadOnlyModelViewSet,mymixins.AddFormMixin):
    """
    API endpoint that allows appeals to be viewed or edited.
    """
    queryset = Appeal.objects.all()
    serializer_class = sirs.AppealSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/appeal_form.html',  # 模板文件
        add_serializer_class=firs.AddAppealSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/appeals/add/
        template: sua/appeals_form.html
        GET: 返回空Appeal序列化器，渲染Appeal创建表单
        POST: 接受Appeal创建表单数据，创建Appeal实例，并重定向至对应的Appeal详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''
        return super(AppealViewSet, self).add(request)

    def perform_add(self, serializer):
        serializer.save(owner=self.request.user)


class ProofViewSet(viewsets.ReadOnlyModelViewSet, mymixins.AddFormMixin):
    """
    API endpoint that allows proofs to be viewed or edited.
    """
    queryset = Proof.objects.all()
    serializer_class = sirs.ProofSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    template_name = None  # 请务必要添加这一行，否则会报错

    @list_route(
        methods=['get', 'post'],  # HTTP METHODS
        renderer_classes=[TemplateHTMLRenderer],  # 使用TemplateHTMLRenderer
        template_name='sua/sua_form.html',  # 模板文件
        add_serializer_class=firs.AddProofSerializer,  # 序列化器
        add_success_url='/',  # 成功后的跳转url
    )
    def add(self, request):
        '''
        url: api/proofs/add/
        template: sua/sua_form.html
        GET: 返回空Proof序列化器，渲染Proof创建表单
        POST: 接受Proof创建表单数据，创建Proof实例，并重定向至对应的Proof详情页面
        表单字段：表单字段请参考REST framework自动生成的表单
        '''


        if request.method == 'GET':
            serializer = self.get_add_serializer()
            return Response({'serializer': serializer})
        elif request.method == 'POST':
            serializer = self.get_add_serializer(data=request.data)
            if serializer.is_valid():
                if not request.data.get('is_offline',False):
                    if not request.data['proof_file']:
                        return Response({'serializer': serializer})
                    self.perform_add(serializer)
                    return self.get_add_response(serializer)
                self.perform_add(serializer)
                return self.get_add_response(serializer)
    def perform_add(self,serializer):
        serializer.save(owner=self.request.user)

#
#
# class JSONResponseMixin(object):
#     """
#     用于返回JSON响应的Mixin
#     """
#     def render_to_json_response(self, context, **response_kwargs):
#         return JsonResponse(
#             self.get_data(context),
#             **response_kwargs
#         )
#
#     def get_data(self, context):
#         msg = {}
#         data = {}
#         if context['msg'] is not None:
#             for k, v in context['msg'].items():
#                 msg[k] = json.loads(serializers.serialize("json", v))
#         else:
#             msg = None
#         data['res'] = context['res']
#         data['msg'] = msg
#         return data
#
#
# class JSONListView(JSONResponseMixin, generic.list.BaseListView):
#     """
#     JSON API的基础View类
#     """
#     def render_to_response(self, context, **response_kwargs):
#         return self.render_to_json_response(context, **response_kwargs)
#
#
# class JSONStudentSuaListView(JSONListView):
#     """
#     查询单个Student的Sua列表的JSON API
#     """
#     def is_itself(self):
#         usr = self.request.user
#         return hasattr(usr, 'student') and usr.student == self.student
#
#     def get_queryset(self):
#         # print(dir(self))
#         self.student = get_object_or_404(Student, pk=self.kwargs['pk'])
#         return Sua.objects.filter(student=self.student, is_valid=True).order_by('date')
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONStudentSuaListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser or self.is_itself() or check_signature(self.request):
#             json_context['res'] = "success"
#             json_context['msg'] = {'sua_list': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONSuaApplicationView(JSONListView):
#     """
#     查询单个Sua对应的Application的JSON API
#     """
#     def is_itself(self):
#         usr = self.request.user
#         return hasattr(usr, 'student') and usr.student == self.sua.student
#
#     def get_queryset(self):
#         self.sua = get_object_or_404(Sua, pk=self.kwargs['pk'])
#         return Sua_Application.objects.filter(sua=self.sua)
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONSuaApplicationView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser or self.is_itself():
#             json_context['res'] = "success"
#             json_context['msg'] = {'application': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONStudentGroupListView(JSONListView):
#     """
#     查询单个Student对应的SuaGroup的JSON API
#     """
#     def is_itself(self):
#         usr = self.request.user
#         return hasattr(usr, 'student') and usr.student == self.student
#
#     def get_queryset(self):
#         self.student = get_object_or_404(Student, pk=self.kwargs['pk'])
#         return self.student.user.groups.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONStudentGroupListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser or self.is_itself():
#             json_context['res'] = "success"
#             json_context['msg'] = {'suagroup_list': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONStudentListView(JSONListView):
#     """
#     查询Student列表的JSON API
#     """
#     def get_queryset(self):
#         return Student.objects.order_by('number')
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONStudentListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser or check_signature(self.request):
#             json_context['res'] = "success"
#             json_context['msg'] = {'student_list': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONApplicationCheckListView(JSONListView):
#     """
#     查询待审核的Application列表的JSON API
#     """
#
#     def get_queryset(self):
#         return Sua_Application.objects.filter(is_checked=False)
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONApplicationCheckListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser:
#             json_context['res'] = "success"
#             json_context['msg'] = {'application_checklist': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONGSuaPublicityListView(JSONListView):
#     """
#     查询全体GSuaPublicity列表的JSON API
#     """
#
#     def get_queryset(self):
#         return GSuaPublicity.objects.order_by('-published_begin_date')
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONGSuaPublicityListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser:
#             json_context['res'] = "success"
#             json_context['msg'] = {'gsua_publicity_list': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONGSuaSuaListView(JSONListView):
#     """
#     查询某一Gsua的Sua列表的JSON API
#     """
#
#     def get_queryset(self):
#         self.gsua = get_object_or_404(GSua, pk=self.kwargs['pk'])
#         return self.gsua.suas.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONGSuaSuaListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser:
#             json_context['res'] = "success"
#             json_context['msg'] = {'sua_list': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONSuaGSuaListView(JSONListView):
#     """
#     查询某一Sua的GSua列表的JSON API
#     """
#
#     def get_queryset(self):
#         self.sua = get_object_or_404(Sua, pk=self.kwargs['pk'])
#         return self.sua.gsua_set.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONSuaGSuaListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser:
#             json_context['res'] = "success"
#             json_context['msg'] = {'gsua': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONSuaGroupAppealListView(JSONListView):
#     """
#     查询某一SuaGroup的Appeal列表的JSON API
#     """
#
#     def get_queryset(self):
#         usr = self.request.user
#         self.group = get_object_or_404(SuaGroup, pk=self.kwargs['pk'])
#         appeals = QuerySet()
#         if usr.is_superuser or self.group.group in usr.groups.all():
#             appeals = Appeal.objects.filter(gsua__group=self.group)
#         return appeals
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONSuaGroupAppealListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser or self.group.group in usr.groups.all():
#             json_context['res'] = "success"
#             json_context['msg'] = {'appeal_list': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class JSONSuaGroupListView(JSONListView):
#     """
#     查询全体SuaGroup的JSON API
#     """
#
#     def get_queryset(self):
#         return SuaGroup.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(JSONSuaGroupListView, self).get_context_data(**kwargs)
#         usr = self.request.user
#         json_context = {}
#         if usr.is_superuser:
#             json_context['res'] = "success"
#             json_context['msg'] = {'suagroup_list': context['object_list']}
#         else:
#             json_context['res'] = "failure"
#             json_context['msg'] = None
#         return json_context
#
#
# class StudentDetailView(UserPassesTestMixin, generic.DetailView):
#     """
#     查询Student详情的View
#     """
#     model = Student
#     template_name = 'sua/student_detail.html'
#     context_object_name = 'student'
#     login_url = '/'
#
#     def test_func(self):
#         usr = self.request.user
#         stu = self.get_object()
#         return usr.is_superuser or usr.pk == stu.pk
#
#     def get_queryset(self):
#         return Student.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(StudentDetailView, self).get_context_data(**kwargs)
#         stu = self.get_object()
#         usr = self.request.user
#         return context
#
#
# class StudentCreate(PermissionRequiredMixin, generic.edit.CreateView):
#     template_name = 'sua/student_form.html'
#     form_class = StudentForm
#     permission_required = 'sua.add_student'
#     login_url = '/'
#
#     def form_valid(self, form):
#         username = str(form.cleaned_data['number'])
#         password = str(form.cleaned_data['initial_password'])
#         group_pk_list = form.cleaned_data['group']
#         if password == '' or None:
#             password = '12345678'
#         user = User.objects.create_user(username=username, password=password)
#
#         for group in user.groups.all():
#             if group.pk not in group_pk_list:
#                 user.groups.remove(group)
#         for group_pk in group_pk_list:
#             user.groups.add(Group.objects.get(pk=int(group_pk)))
#
#         user.save()
#         form.instance.user = user
#         return super(StudentCreate, self).form_valid(form)
#
#     def get_initial(self):
#         initial = super(StudentCreate, self).get_initial()
#         initial['group'] = initial.get('group', [])
#         pk = SuaGroup.objects.get(name='个人用户').group.pk
#         if pk not in initial['group']:
#             initial['group'].append(pk)
#         return initial
#
#
# class StudentUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
#     template_name = 'sua/student_form.html'
#     form_class = StudentForm
#     model = Student
#     permission_required = 'sua.change_student'
#     login_url = '/'
#
#     def form_valid(self, form):
#         user = get_object_or_404(User, pk=form.instance.pk)
#         username = form.cleaned_data['number']
#         password = form.cleaned_data['initial_password']
#         group_pk_list = form.cleaned_data['group']
#         if not(password == '' or None):
#             user.password = password
#         user.username = username
#
#         for group in user.groups.all():
#             if group.pk not in group_pk_list:
#                 user.groups.remove(group)
#         for group_pk in group_pk_list:
#             user.groups.add(Group.objects.get(pk=int(group_pk)))
#
#         user.save()
#         return super(StudentUpdate, self).form_valid(form)
#
#     def get_form_kwargs(self):
#         kwargs = super(StudentUpdate, self).get_form_kwargs()
#         kwargs['instance'] = self.get_object()
#         return kwargs
#
#     def get_initial(self):
#         initial = super(StudentUpdate, self).get_initial()
#         initial['group'] = initial.get('group', [])
#         groups = (self.get_object()).user.groups.all()
#         for group in groups:
#             initial['group'].append(group.pk)
#         return initial
#
#
# class StudentDelete(PermissionRequiredMixin, generic.edit.DeleteView):
#     model = Student
#     success_url = reverse_lazy('sua:admin-index')
#     permission_required = 'sua.delete_student'
#     login_url = '/'
#
#
# class Sua_ApplicationDetailView(UserPassesTestMixin, generic.DetailView):
#     """
#     查询Application详情的View
#     """
#     model = Sua_Application
#     template_name = 'sua/application_detail.html'
#     context_object_name = 'sa'
#     login_url = '/'
#
#     def test_func(self):
#         usr = self.request.user
#         application = self.get_object()
#         return usr.is_superuser or usr.student.pk == application.sua.student.pk
#
#     def get_queryset(self):
#         return Sua_Application.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(Sua_ApplicationDetailView, self).get_context_data(**kwargs)
#         sa = self.get_object()
#
#         year = sa.date.year
#         month = sa.date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#
#         context['year_before'] = year_before
#         context['year_after'] = year_after
#         return context
#
#
# class Sua_ApplicationCreate(PermissionRequiredMixin, generic.edit.CreateView):
#     template_name = 'sua/sua_application_form.html'
#     form_class = SuaForm
#     permission_required = 'sua.add_sua_application'
#     login_url = '/'
#     success_url = '/'
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         if context['proofForm'].is_valid() and\
#                 context['sua_ApplicationForm'].is_valid():
#             if context['proofForm'].cleaned_data['is_offline']:
#                 offlineProofSet = Proof.objects.filter(is_offline=True)
#                 if offlineProofSet.count == 0:
#                     assert(User.objects.filter(is_superuser=True).count != 0)
#                     proof = Proof.objects.create(
#                         user=User.objects.filter(is_superuser=True)[0],
#                         date=timezone.now(),
#                         is_offline=True,
#                     )
#                     proof.save()
#                 else:
#                     proof = offlineProofSet[0]
#             else:
#                 proof = context['proofForm'].save(commit=False)
#             sua = form.save(commit=False)
#             sua_Application = context['sua_ApplicationForm'].save(commit=False)
#             # 处理proof
#             if not context['proofForm'].cleaned_data['is_offline']:
#                 proof.user = self.request.user
#                 proof.date = timezone.now()
#                 proof.save()
#             # 处理sua
#             sua.student = self.stu
#             sua.last_time_suahours = 0.0
#             sua.is_valid = True
#             sua.save()
#             # 处理sua_Application
#             sua_Application.sua = sua
#             sua_Application.date = timezone.now()
#             sua_Application.proof = proof
#             sua_Application.is_checked = True
#             sua_Application.save()
#             self.success_url = reverse('sua:application-detail', kwargs={'pk': sua_Application.pk})
#         else:
#             self.form_invalid()
#         return super(Sua_ApplicationCreate, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(Sua_ApplicationCreate, self).get_context_data(**kwargs)
#         self.stu = get_object_or_404(Student, pk=self.kwargs['pk'])
#         date = timezone.now()
#         year = date.year
#         month = date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#
#         if self.request.method == 'POST':
#             proofForm = ProofForm(self.request.POST, self.request.FILES, prefix='proofForm')
#             sua_ApplicationForm = Sua_ApplicationForm(
#                 self.request.POST,
#                 prefix='sua_ApplicationForm',
#             )
#         else:
#             proofForm = ProofForm(prefix='proofForm')
#             sua_ApplicationForm = Sua_ApplicationForm(
#                 prefix='sua_ApplicationForm',
#             )
#         context['suaForm'] = context['form']
#         context['proofForm'] = proofForm
#         context['sua_ApplicationForm'] = sua_ApplicationForm
#         context['apply_date'] = date.date()
#         context['apply_year_before'] = year_before
#         context['apply_year_after'] = year_after
#         context['stu_name'] = self.stu.name
#         context['stu_number'] = self.stu.number
#         return context
#
#
# class Sua_ApplicationUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
#     template_name = 'sua/sua_application_form.html'
#     form_class = Sua_ApplicationForm
#     permission_required = 'sua.change_sua_application'
#     login_url = '/'
#     success_url = '/'
#
#     def get_queryset(self):
#         return Sua_Application.objects.all()
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         if context['proofForm'].is_valid() and\
#                 context['suaForm'].is_valid():
#             if context['proofForm'].cleaned_data['is_offline']:
#                 offlineProofSet = Proof.objects.filter(is_offline=True)
#                 if offlineProofSet.count == 0:
#                     assert(User.objects.filter(is_superuser=True).count != 0)
#                     proof = Proof.objects.create(
#                         user=User.objects.filter(is_superuser=True)[0],
#                         date=timezone.now(),
#                         is_offline=True,
#                     )
#                     proof.save()
#                 else:
#                     proof = offlineProofSet[0]
#             else:
#                 proof = context['proofForm'].save(commit=False)
#                 if context['proofForm'].cleaned_data['proof_file'] is None:
#                     proof = self.application.proof
#             sua = context['suaForm'].save(commit=False)
#             sua_Application = context['sua_ApplicationForm'].save(commit=False)
#             # 处理proof
#             if not (context['proofForm'].cleaned_data['is_offline'] or context['proofForm'].cleaned_data['proof_file'] is None):
#                 proof.user = self.request.user
#                 proof.date = timezone.now()
#                 proof.save()
#             # 处理sua
#             self.sua.group = sua.group
#             self.sua.title = sua.title
#             self.sua.team = sua.team
#             self.sua.date = sua.date
#             self.sua.suahours = sua.suahours
#             self.sua.save()
#             # 处理sua_Application
#             self.application.detail = sua_Application.detail
#             self.application.contact = sua_Application.contact
#             sua_Application.proof = proof
#             self.application.proof = sua_Application.proof
#             self.application.save()
#             self.success_url = reverse('sua:application-detail', kwargs={'pk': self.application.pk})
#         else:
#             self.form_invalid(form)
#         return super(Sua_ApplicationUpdate, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(Sua_ApplicationUpdate, self).get_context_data(**kwargs)
#         self.application = self.get_object()
#         self.sua = self.application.sua
#         self.stu = self.sua.student
#         date = self.application.date
#         year = date.year
#         month = date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#
#         if self.request.method == 'POST':
#             proofForm = ProofForm(self.request.POST, self.request.FILES)
#             suaForm = SuaForm(
#                 self.request.POST,
#                 prefix='suaForm',
#             )
#         else:
#             proofForm = ProofForm(prefix='proofForm', instance=self.application.proof)
#             suaForm = SuaForm(
#                 prefix='suaForm',
#                 instance=self.sua
#             )
#         context['suaForm'] = suaForm
#         context['proofForm'] = proofForm
#         context['sua_ApplicationForm'] = context['form']
#         context['apply_date'] = date.date()
#         context['apply_year_before'] = year_before
#         context['apply_year_after'] = year_after
#         context['stu_name'] = self.stu.name
#         context['stu_number'] = self.stu.number
#         return context
#
#
# class Sua_ApplicationDelete(PermissionRequiredMixin, generic.edit.DeleteView):
#     model = Sua_Application
#     success_url = reverse_lazy('sua:admin-index')
#     permission_required = 'sua.delete_sua_application'
#     login_url = '/'
#
#
# class Sua_ApplicationCheck(PermissionRequiredMixin, generic.edit.UpdateView):
#     template_name = 'sua/sua_application_check.html'
#     form_class = Sua_ApplicationCheckForm
#     permission_required = 'sua.change_sua_application'
#     login_url = '/'
#     success_url = '/'
#
#     def get_queryset(self):
#         return Sua_Application.objects.all()
#
#     def form_valid(self, form):
#         self.application = self.get_object()
#         form.instance.is_checked = True
#         self.application.sua.is_valid = form.cleaned_data['is_passed']
#         self.application.sua.save()
#         self.success_url = reverse('sua:application-detail', kwargs={'pk': self.application.pk})
#         return super(Sua_ApplicationCheck, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(Sua_ApplicationCheck, self).get_context_data(**kwargs)
#         self.application = self.get_object()
#         date = self.application.date
#         year = date.year
#         month = date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#
#         context['year_before'] = year_before
#         context['year_after'] = year_after
#         context['sa'] = self.application
#         return context
#
#     def get_initial(self):
#         initial = super(Sua_ApplicationCheck, self).get_initial()
#         initial['is_passed'] = self.get_object().sua.is_valid
#         return initial
#
#
# class GSuaPublicityDetailView(UserPassesTestMixin, generic.DetailView):
#     """
#     查询GSuaPublicity详情的View
#     """
#     model = GSuaPublicity
#     template_name = 'sua/gsua_publicity_detail.html'
#     context_object_name = 'gsuap'
#     login_url = '/'
#
#     def test_func(self):
#         flag = False
#         usr = self.request.user
#         groups = usr.groups.all()
#         gsuap = self.get_object()
#         if gsuap.gsua.group.group in groups:
#             flag = True
#         return usr.is_superuser or flag
#
#     def get_queryset(self):
#         return GSuaPublicity.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(GSuaPublicityDetailView, self).get_context_data(**kwargs)
#         gsuap = self.get_object()
#
#         year = gsuap.gsua.date.year
#         month = gsuap.gsua.date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#
#         context['year_before'] = year_before
#         context['year_after'] = year_after
#         return context
#
#
# class GSuaPublicityCreate(PermissionRequiredMixin, generic.edit.CreateView):
#     template_name = 'sua/gsua_publicity_form.html'
#     form_class = GSuaPublicityForm
#     permission_required = 'sua.add_gsuapublicity'
#     login_url = '/'
#     success_url = '/'
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         usr = self.request.user
#         date = form.cleaned_data['date']
#         if usr.is_superuser:
#             group = SuaGroup.objects.get(pk=2)
#         else:
#             group = (usr.groups.order_by('-suagroup__rank').first()).suagroup
#         suas = []
#         gsuap = form.save(commit=False)
#         if context['formset'].is_valid():
#             for suaform in context['formset']:
#                 if suaform.cleaned_data != {}:
#                     sua = suaform.save(commit=False)
#                     sua.group = group
#                     sua.title = gsuap.title
#                     sua.date = date
#                     sua.last_time_suahours = 0.0
#                     sua.is_valid = True
#                     sua.save()
#                     suas.append(sua)
#             print(gsuap.title)
#             gsua = GSua.objects.create(title=gsuap.title, group=group, date=date, is_valid=True)
#             for sua in suas:
#                 gsua.suas.add(sua)
#             gsua.save()
#             gsuap.gsua = gsua
#             gsuap.user = usr
#             gsuap.save()
#             self.success_url = reverse('sua:gsuap-detail', kwargs={'pk': gsuap.pk})
#         else:
#             self.form_invalid(form)
#         return super(GSuaPublicityCreate, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(GSuaPublicityCreate, self).get_context_data(**kwargs)
#         SuaFormSet = modelformset_factory(
#             Sua, fields=('student', 'team', 'suahours'), extra=0,
#             widgets={
#                 'student': forms.Select(attrs={
#                     'class': 'form-control'
#                 }),
#                 'team': forms.TextInput(attrs={
#                     'class': 'form-control'
#                 }),
#                 'suahours': forms.TextInput(attrs={
#                     'class': 'form-control',
#                     'placeholder': '请输入公益时数',
#                 })
#             }
#         )
#         date = timezone.now()
#         year = date.year
#         month = date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#
#         if self.request.method == 'POST':
#             formset = SuaFormSet(self.request.POST, self.request.FILES)
#         else:
#             formset = SuaFormSet(queryset=Sua.objects.none())
#         context['formset'] = formset
#         context['apply_year_before'] = year_before
#         context['apply_year_after'] = year_after
#         context['title'] = '创建新的公益时活动'
#         context['description'] = '您可以在这里创建新的公益时活动'
#         return context
#
#
# class GSuaPublicityUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
#     template_name = 'sua/gsua_publicity_form.html'
#     form_class = GSuaPublicityForm
#     permission_required = 'sua.change_gsuapublicity'
#     login_url = '/'
#     success_url = '/'
#
#     def get_queryset(self):
#         return GSuaPublicity.objects.all()
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         usr = self.request.user
#         date = form.cleaned_data['date']
#         group = self.get_object().gsua.group
#         suas = []
#         gsuap = form.save(commit=False)
#         if context['formset'].is_valid():
#             for suaform in context['formset']:
#                 if suaform.cleaned_data != {} and (not suaform.cleaned_data['DELETE']):
#                     sua = suaform.save(commit=False)
#                     sua.group = group
#                     sua.title = gsuap.title
#                     sua.date = date
#                     sua.is_valid = True
#                     sua.save()
#                     suas.append(sua)
#             gsua = self.get_object().gsua
#             for sua in gsua.suas.all():
#                 if sua not in suas:
#                     gsua.suas.remove(sua)
#                     sua.is_valid = False
#                     sua.save()
#                     sua.delete()
#             for sua in suas:
#                 if sua not in gsua.suas.all():
#                     gsua.suas.add(sua)
#
#             gsua.title = gsuap.title
#             gsua.date = date
#             gsua.save()
#             self.success_url = reverse('sua:gsuap-detail', kwargs={'pk': self.get_object().pk})
#         else:
#             print('invalid')
#             self.form_invalid(form)
#         return super(GSuaPublicityUpdate, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(GSuaPublicityUpdate, self).get_context_data(**kwargs)
#         SuaFormSet = modelformset_factory(
#             Sua, fields=('student', 'team', 'suahours'), extra=0, can_delete=True,
#             widgets={
#                 'student': forms.Select(attrs={
#                     'class': 'form-control'
#                 }),
#                 'team': forms.TextInput(attrs={
#                     'class': 'form-control'
#                 }),
#                 'suahours': forms.TextInput(attrs={
#                     'class': 'form-control',
#                     'placeholder': '请输入公益时数',
#                 }),
#                 'DELETE': forms.CheckboxInput(attrs={
#                     'class': 'checkbox',
#                     'placeholder': '请输入公益时数',
#                 }),
#             }
#         )
#         gsuap = self.get_object()
#         date = gsuap.published_begin_date
#         year = date.year
#         month = date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#
#         if self.request.method == 'POST':
#             formset = SuaFormSet(self.request.POST, self.request.FILES)
#         else:
#             formset = SuaFormSet(queryset=gsuap.gsua.suas.all())
#         context['formset'] = formset
#         context['apply_year_before'] = year_before
#         context['apply_year_after'] = year_after
#         context['title'] = '修改公益时活动'
#         context['description'] = '您正在修改公益时活动'
#         return context
#
#     def get_initial(self):
#         initial = super(GSuaPublicityUpdate, self).get_initial()
#         initial['date'] = self.get_object().gsua.date
#         return initial
#
#
# class GSuaDelete(PermissionRequiredMixin, generic.edit.DeleteView):
#     model = GSua
#     success_url = reverse_lazy('sua:admin-index')
#     permission_required = 'sua.delete_gsua'
#     login_url = '/'
#
#
# class AppealDetailView(UserPassesTestMixin, generic.DetailView):
#     """
#     查询Appeal详情的View
#     """
#     model = Appeal
#     template_name = 'sua/appeal_detail.html'
#     context_object_name = 'appealForm'
#     login_url = '/'
#
#     def test_func(self):
#         flag = False
#         usr = self.request.user
#         appeal = self.get_object()
#         if appeal.student.pk == usr.pk:
#             flag = True
#         return usr.is_superuser or flag
#
#     def get_queryset(self):
#         return Appeal.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(AppealDetailView, self).get_context_data(**kwargs)
#         appeal = self.get_object()
#         gsuap = appeal.gsua.gsuapublicity_set.first()
#
#         year = appeal.date.year
#         month = appeal.gsua.date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#
#         context['year_before'] = year_before
#         context['year_after'] = year_after
#         context['gsuap'] = gsuap
#         return context
#
#
# class AppealUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
#     template_name = 'sua/appeal_form.html'
#     form_class = AppealForm
#     model = Appeal
#     permission_required = 'sua.change_appeal'
#     login_url = '/'
#     success_url = '/'
#
#     def form_valid(self, form):
#         # 也许这个函数是用不着的.
#         appeal = get_object_or_404(Appeal, pk=form.instance.pk)
#         return super(AppealUpdate, self).form_valid(form)
#
#     def get_form_kwargs(self):
#         kwargs = super(AppealUpdate, self).get_form_kwargs()
#         kwargs['instance'] = self.get_object()
#         return kwargs
#
#
# class AppealCheck(PermissionRequiredMixin, generic.edit.UpdateView):
#     template_name = 'sua/appeal_check.html'
#     form_class = AppealCheckForm
#     permission_required = 'sua.change_appeal'
#     login_url = '/'
#     success_url = '/'
#
#     def get_queryset(self):
#         return Appeal.objects.all()
#
#     def form_valid(self, form):
#         self.appeal = self.get_object()
#         form.instance.is_checked = True
#         return super(AppealCheck, self).form_valid(form)
#
#
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['user_password']
            loginstatus = form.cleaned_data['loginstatus']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if(loginstatus):
                    request.session.set_expiry(15 * 24 * 3600)
                else:
                    request.session.set_expiry(0)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login')
    else:
        form = LoginForm()
    return render(request, 'sua/login.html', {'form': form})
#
#
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
#
#
@login_required
def index(request):
    return render(request, 'sua/index.html', {
    })
#
#
# @login_required
# def apply_sua(request):
#     usr = request.user
#     stu = None
#     if hasattr(usr, 'student'):
#         stu = usr.student
#         name = stu.name
#         number = stu.number
#         suahours = stu.suahours
#     else:
#         if usr.is_staff:
#             name = 'Admin.' + usr.username
#         else:
#             name = 'NoStuInfo.' + usr.username
#         number = '------'
#     date = timezone.now()
#     year = date.year
#     month = date.month
#     if month < 9:
#         year_before = year - 1
#         year_after = year
#     else:
#         year_before = year
#         year_after = year + 1
#
#     # 表单处理
#     if request.method == 'POST':
#         suaForm = SuaForm(request.POST, prefix='suaForm')
#         proofForm = ProofForm(request.POST, request.FILES, prefix='proofForm')
#         sua_ApplicationForm = Sua_ApplicationForm(
#             request.POST,
#             prefix='sua_ApplicationForm',
#         )
#         if suaForm.is_valid() and\
#                 proofForm.is_valid() and\
#                 sua_ApplicationForm.is_valid() and\
#                 stu is not None:
#             # 生成Models
#             if proofForm.cleaned_data['is_offline']:
#                 offlineProofSet = Proof.objects.filter(is_offline=True)
#                 if offlineProofSet.count == 0:
#                     assert(User.objects.filter(is_superuser=True).count != 0)
#                     proof = Proof.objects.create(
#                         user=User.objects.filter(is_superuser=True)[0],
#                         date=date,
#                         is_offline=True,
#                     )
#                     proof.save()
#                 else:
#                     proof = offlineProofSet[0]
#             else:
#                 proof = proofForm.save(commit=False)
#             sua = suaForm.save(commit=False)
#             sua_Application = sua_ApplicationForm.save(commit=False)
#             # 处理proof
#             if not proofForm.cleaned_data['is_offline']:
#                 proof.user = usr
#                 proof.date = date
#                 proof.save()
#             # 处理sua
#             sua.student = stu
#             sua.last_time_suahours = 0.0
#             sua.is_valid = False
#             sua.save()
#             # 处理sua_Application
#             sua_Application.sua = sua
#             sua_Application.date = date
#             sua_Application.proof = proof
#             sua_Application.is_checked = False
#             sua_Application.save()
#             return HttpResponseRedirect('/')
#     else:
#         suaForm = SuaForm(prefix='suaForm')
#         proofForm = ProofForm(prefix='proofForm')
#         sua_ApplicationForm = Sua_ApplicationForm(
#             prefix='sua_ApplicationForm',
#         )
#
#     return render(request, 'sua/apply_sua.html', {
#         'stu_name': name,
#         'stu_number': number,
#         'stu_suahours': suahours,
#         'apply_date': date.date(),
#         'apply_year_before': year_before,
#         'apply_year_after': year_after,
#         'proofForm': proofForm,
#         'suaForm': suaForm,
#         'sua_ApplicationForm': sua_ApplicationForm,
#     })
#
#
# @login_required
# def appeal_for(request):
#     usr = request.user
#     stu = None
#     gsuap = GSuaPublicity.objects.get(pk=int(request.GET.get('gsuap_id')))
#     if hasattr(usr, 'student'):
#         stu = usr.student
#         name = stu.name
#         number = stu.number
#         suahours = stu.suahours
#     else:
#         if usr.is_staff:
#             name = 'Admin.' + usr.username
#         else:
#             name = 'NoStuInfo.' + usr.username
#         number = '------'
#     date = timezone.now()
#     year = date.year
#     month = date.month
#     if month < 9:
#         year_before = year - 1
#         year_after = year
#     else:
#         year_before = year
#         year_after = year + 1
#     # 表单处理
#     if request.method == 'POST':
#         print(gsuap)
#         appealForm = AppealForm(request.POST, prefix='appealForm')
#         if appealForm.is_valid() and\
#                 stu is not None and\
#                 gsuap is not None:
#             if date <= gsuap.published_end_date:
#                 # 生成Models
#                 appeal = appealForm.save(commit=False)
#                 # 处理appeal
#                 appeal.student = stu
#                 appeal.date = date
#                 appeal.gsua = gsuap.gsua
#                 appeal.is_checked = False
#                 appeal.feedback = ''
#                 appeal.save()
#                 return HttpResponseRedirect('/')
#     else:
#         print(gsuap)
#         appealForm = AppealForm(prefix='appealForm')
#     return render(request, 'sua/appeal_for.html', {
#         'stu_name': name,
#         'stu_number': number,
#         'stu_suahours': suahours,
#         'appealYearBefore': year_before,
#         'appealYearAfter': year_after,
#         'appealDate': date.date(),
#         'appealForm': appealForm,
#         'gsuap': gsuap,
#     })
#
#
# class ApplicationDetailView(generic.DetailView):
#     model = Sua_Application
#     template_name = 'sua/application_detail.html'
#     context_object_name = 'sa'
#
#     def get_queryset(self):
#         user = self.request.user
#         return Sua_Application.objects.filter(
#             sua__student__user=user
#         )
#
#     def get_context_data(self, **kwargs):
#         context = super(ApplicationDetailView, self).get_context_data(**kwargs)
#         sa = self.get_object()
#         usr = self.request.user
#         stu = None
#         suahours = 0
#         if hasattr(usr, 'student'):
#             stu = usr.student
#             name = stu.name
#             number = stu.number
#             suahours = stu.suahours
#         else:
#             if usr.is_staff:
#                 name = 'Admin.' + usr.username
#             else:
#                 name = 'NoStuInfo.' + usr.username
#             number = '------'
#         year = sa.date.year
#         month = sa.date.month
#         if month < 9:
#             year_before = year - 1
#             year_after = year
#         else:
#             year_before = year
#             year_after = year + 1
#         print(context)
#         context['year_before'] = year_before
#         context['year_after'] = year_after
#         context['stu_name'] = name
#         context['stu_number'] = number
#         context['stu_suahours'] = suahours
#         return context
#
#
# @login_required
# def adminIndex(request):
#     usr = request.user
#     if not usr.is_staff:
#         return HttpResponseRedirect('/')
#     else:
#         students = []  # 全体学生
#         gsuaps = []  # 全体活动公示
#         appeals = []  # 全体申诉
#
#         # 获取全体学生
#         i = 0
#         for stu in Student.objects.order_by('number'):
#             i += 1
#             students.append((i, stu))
#         # 获取全体活动公示
#         i = 0
#         for gsuap in GSuaPublicity.objects.order_by('-published_begin_date'):
#             i += 1
#             gsuaps.append((i, gsuap))
#         # 获取全体申诉
#         i = 0
#         for appeal in Appeal.objects.order_by('-date'):
#             i += 1
#             appeals.append((i, appeal))
#
#         # 返回render
#         return render(request, 'sua/admin_index.html', {
#             'students': students,
#             'gsuaps': gsuaps,
#             'appeals': appeals,
#         })
#
#
# def playMFS(request):
#     SuaFormSet = modelformset_factory(
#         Sua, fields=('student', 'team', 'suahours'), extra=1,
#         widgets={
#             'student': forms.Select(attrs={
#                 'class': 'form-control'
#             }),
#             'team': forms.TextInput(attrs={
#                 'class': 'form-control'
#             }),
#             'suahours': forms.TextInput(attrs={
#                 'class': 'form-control'
#             })
#         }
#     )
#     if request.method == 'POST':
#         formset = SuaFormSet(request.POST, request.FILES)
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data != {}:
#                     print(form.cleaned_data)
#                     sua = form.save(commit=False)
#                     sua.group = SuaGroup.objects.all()[0]
#                     sua.title = '批量测试'
#                     sua.date = timezone.now()
#                     sua.last_time_suahours = 0
#                     sua.is_valid = False
#                     sua.save()
#     else:
#         formset = SuaFormSet(queryset=Sua.objects.none())
#     return render(request, 'sua/playMFS.html', {'formset': formset})
