from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy, reverse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User, Group
from .forms import LoginForm, SuaForm, Sua_ApplicationForm, ProofForm, AppealForm, StudentForm
from .models import Sua, Proof, Sua_Application, GSuaPublicity, GSua, Student, Appeal, SuaGroup
import json


class JSONResponseMixin(object):
    """
    用于返回JSON响应的Mixin
    """
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        msg = {}
        data = {}
        if context['msg'] is not None:
            for k, v in context['msg'].items():
                msg[k] = json.loads(serializers.serialize("json", v))
        else:
            msg = None
        data['res'] = context['res']
        data['msg'] = msg
        return data


class JSONListView(JSONResponseMixin, generic.list.BaseListView):
    """
    JSON API的基础View类
    """
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class JSONStudentSuaListView(JSONListView):
    """
    查询单个Student的Sua列表的JSON API
    """
    def is_itself(self):
        usr = self.request.user
        return hasattr(usr, 'student') and usr.student == self.student

    def get_queryset(self):
        self.student = get_object_or_404(Student, pk=self.args[0])
        return Sua.objects.filter(student=self.student, is_valid=True)

    def get_context_data(self, **kwargs):
        context = super(JSONStudentSuaListView, self).get_context_data(**kwargs)
        usr = self.request.user
        json_context = {}
        if usr.is_superuser or self.is_itself():
            json_context['res'] = "success"
            json_context['msg'] = {'sua_list': context['object_list']}
        else:
            json_context['res'] = "failure"
            json_context['msg'] = None
        return json_context


class JSONSuaApplicationView(JSONListView):
    """
    查询单个Sua对应的Application的JSON API
    """
    def is_itself(self):
        usr = self.request.user
        return hasattr(usr, 'student') and usr.student == self.sua.student

    def get_queryset(self):
        self.sua = get_object_or_404(Sua, pk=self.args[0])
        return Sua_Application.objects.filter(sua=self.sua)

    def get_context_data(self, **kwargs):
        context = super(JSONSuaApplicationView, self).get_context_data(**kwargs)
        usr = self.request.user
        json_context = {}
        if usr.is_superuser or self.is_itself():
            json_context['res'] = "success"
            json_context['msg'] = {'sua_application': context['object_list']}
        else:
            json_context['res'] = "failure"
            json_context['msg'] = None
        return json_context


class JSONStudentListView(JSONListView):
    """
    查询Student列表的JSON API
    """
    def get_queryset(self):
        return Student.objects.order_by('number')

    def get_context_data(self, **kwargs):
        context = super(JSONStudentListView, self).get_context_data(**kwargs)
        usr = self.request.user
        json_context = {}
        if usr.is_superuser:
            json_context['res'] = "success"
            json_context['msg'] = {'student_list': context['object_list']}
        else:
            json_context['res'] = "failure"
            json_context['msg'] = None
        return json_context


class StudentDetailView(UserPassesTestMixin, generic.DetailView):
    """
    查询Student详情的View
    """
    model = Student
    template_name = 'sua/student_detail.html'
    context_object_name = 'student'
    login_url = '/'

    def test_func(self):
        usr = self.request.user
        stu = self.get_object()
        return usr.is_superuser or usr.pk == stu.pk

    def get_queryset(self):
        return Student.objects.all()

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        stu = self.get_object()
        usr = self.request.user
        return context


class StudentCreate(PermissionRequiredMixin, generic.edit.CreateView):
    template_name = 'sua/student_form.html'
    form_class = StudentForm
    permission_required = 'sua.add_student'
    login_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['number']
        password = form.cleaned_data['initial_password']
        group_pk_list = form.cleaned_data['group']
        if password == '' or None:
            password = '12345678'
        user = User.objects.create_user(username=username, password=password)

        for group in user.groups.all():
            if group.pk not in group_pk_list:
                user.groups.remove(group)
        for group_pk in group_pk_list:
            user.groups.add(Group.objects.get(pk=int(group_pk)))

        user.save()
        form.instance.user = user
        return super(StudentCreate, self).form_valid(form)

    def get_initial(self):
        initial = super(StudentCreate, self).get_initial()
        initial['group'] = initial.get('group', [])
        pk = SuaGroup.objects.get(name='个人用户').group.pk
        if pk not in initial['group']:
            initial['group'].append(pk)
        return initial


class StudentUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
    template_name = 'sua/student_form.html'
    form_class = StudentForm
    model = Student
    permission_required = 'sua.change_student'
    login_url = '/'

    def form_valid(self, form):
        user = get_object_or_404(User, pk=form.instance.pk)
        username = form.cleaned_data['number']
        password = form.cleaned_data['initial_password']
        group_pk_list = form.cleaned_data['group']
        if not(password == '' or None):
            user.password = password
        user.username = username

        for group in user.groups.all():
            if group.pk not in group_pk_list:
                user.groups.remove(group)
        for group_pk in group_pk_list:
            user.groups.add(Group.objects.get(pk=int(group_pk)))

        user.save()
        return super(StudentUpdate, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(StudentUpdate, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_initial(self):
        initial = super(StudentUpdate, self).get_initial()
        initial['group'] = initial.get('group', [])
        groups = (self.get_object()).user.groups.all()
        for group in groups:
            initial['group'].append(group.pk)
        return initial


class StudentDelete(PermissionRequiredMixin, generic.edit.DeleteView):
    model = Student
    success_url = reverse_lazy('sua:admin-index')
    permission_required = 'sua.delete_student'
    login_url = '/'


class Sua_ApplicationDetailView(UserPassesTestMixin, generic.DetailView):
    """
    查询Application详情的View
    """
    model = Sua_Application
    template_name = 'sua/application_detail.html'
    context_object_name = 'sa'
    login_url = '/'

    def test_func(self):
        usr = self.request.user
        application = self.get_object()
        return usr.is_superuser or usr.pk == application.sua.student.pk

    def get_queryset(self):
        return Sua_Application.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Sua_ApplicationDetailView, self).get_context_data(**kwargs)
        sa = self.get_object()

        year = sa.date.year
        month = sa.date.month
        if month < 9:
            year_before = year - 1
            year_after = year
        else:
            year_before = year
            year_after = year + 1

        context['year_before'] = year_before
        context['year_after'] = year_after
        return context


class Sua_ApplicationCreate(PermissionRequiredMixin, generic.edit.CreateView):
    template_name = 'sua/sua_application_form.html'
    form_class = SuaForm
    permission_required = 'sua.add_sua_application'
    login_url = '/'
    success_url = '/'

    def form_valid(self, form):
        context = self.get_context_data()
        if context['proofForm'].is_valid() and\
                context['sua_ApplicationForm'].is_valid():
            if context['proofForm'].cleaned_data['is_offline']:
                offlineProofSet = Proof.objects.filter(is_offline=True)
                if offlineProofSet.count == 0:
                    assert(User.objects.filter(is_superuser=True).count != 0)
                    proof = Proof.objects.create(
                        user=User.objects.filter(is_superuser=True)[0],
                        date=timezone.now(),
                        is_offline=True,
                    )
                    proof.save()
                else:
                    proof = offlineProofSet[0]
            else:
                proof = context['proofForm'].save(commit=False)
            sua = form.save(commit=False)
            sua_Application = context['sua_ApplicationForm'].save(commit=False)
            # 处理proof
            if not context['proofForm'].cleaned_data['is_offline']:
                proof.user = self.request.user
                proof.date = timezone.now()
                proof.save()
            # 处理sua
            sua.student = self.stu
            sua.last_time_suahours = 0.0
            sua.is_valid = True
            sua.save()
            # 处理sua_Application
            sua_Application.sua = sua
            sua_Application.date = timezone.now()
            sua_Application.proof = proof
            sua_Application.is_checked = True
            sua_Application.save()
            self.success_url = reverse('sua:application-detail', kwargs={'pk': sua_Application.pk})
        else:
            self.form_invalid()
        return super(Sua_ApplicationCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Sua_ApplicationCreate, self).get_context_data(**kwargs)
        self.stu = get_object_or_404(Student, pk=self.args[0])
        date = timezone.now()
        year = date.year
        month = date.month
        if month < 9:
            year_before = year - 1
            year_after = year
        else:
            year_before = year
            year_after = year + 1

        if self.request.method == 'POST':
            proofForm = ProofForm(self.request.POST, self.request.FILES, prefix='proofForm')
            sua_ApplicationForm = Sua_ApplicationForm(
                self.request.POST,
                prefix='sua_ApplicationForm',
            )
        else:
            proofForm = ProofForm(prefix='proofForm')
            sua_ApplicationForm = Sua_ApplicationForm(
                prefix='sua_ApplicationForm',
            )
        context['suaForm'] = context['form']
        context['proofForm'] = proofForm
        context['sua_ApplicationForm'] = sua_ApplicationForm
        context['apply_date'] = date.date()
        context['apply_year_before'] = year_before
        context['apply_year_after'] = year_after
        context['stu_name'] = self.stu.name
        context['stu_number'] = self.stu.number
        return context


class Sua_ApplicationUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
    template_name = 'sua/sua_application_form.html'
    form_class = Sua_ApplicationForm
    permission_required = 'sua.change_sua_application'
    login_url = '/'
    success_url = '/'

    def get_queryset(self):
        return Sua_Application.objects.all()

    def form_valid(self, form):
        context = self.get_context_data()
        if context['proofForm'].is_valid() and\
                context['suaForm'].is_valid():
            if context['proofForm'].cleaned_data['is_offline']:
                offlineProofSet = Proof.objects.filter(is_offline=True)
                if offlineProofSet.count == 0:
                    assert(User.objects.filter(is_superuser=True).count != 0)
                    proof = Proof.objects.create(
                        user=User.objects.filter(is_superuser=True)[0],
                        date=timezone.now(),
                        is_offline=True,
                    )
                    proof.save()
                else:
                    proof = offlineProofSet[0]
            else:
                proof = context['proofForm'].save(commit=False)
                if context['proofForm'].cleaned_data['proof_file'] is None:
                    proof = self.application.proof
            sua = context['suaForm'].save(commit=False)
            sua_Application = context['sua_ApplicationForm'].save(commit=False)
            # 处理proof
            if not (context['proofForm'].cleaned_data['is_offline'] or context['proofForm'].cleaned_data['proof_file'] is None):
                proof.user = self.request.user
                proof.date = timezone.now()
                proof.save()
            # 处理sua
            self.sua.group = sua.group
            self.sua.title = sua.title
            self.sua.team = sua.team
            self.sua.date = sua.date
            self.sua.suahours = sua.suahours
            self.sua.save()
            # 处理sua_Application
            self.application.detail = sua_Application.detail
            self.application.contact = sua_Application.contact
            sua_Application.proof = proof
            self.application.proof = sua_Application.proof
            self.application.save()
            self.success_url = reverse('sua:application-detail', kwargs={'pk': self.application.pk})
        else:
            self.form_invalid(form)
        return super(Sua_ApplicationUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Sua_ApplicationUpdate, self).get_context_data(**kwargs)
        self.application = self.get_object()
        self.sua = self.application.sua
        self.stu = self.sua.student
        date = self.application.date
        year = date.year
        month = date.month
        if month < 9:
            year_before = year - 1
            year_after = year
        else:
            year_before = year
            year_after = year + 1

        if self.request.method == 'POST':
            proofForm = ProofForm(self.request.POST, self.request.FILES, prefix='proofForm')
            suaForm = SuaForm(
                self.request.POST,
                prefix='suaForm',
            )
        else:
            proofForm = ProofForm(prefix='proofForm', instance=self.application.proof)
            suaForm = SuaForm(
                prefix='suaForm',
                instance=self.sua
            )
        context['suaForm'] = suaForm
        context['proofForm'] = proofForm
        context['sua_ApplicationForm'] = context['form']
        context['apply_date'] = date.date()
        context['apply_year_before'] = year_before
        context['apply_year_after'] = year_after
        context['stu_name'] = self.stu.name
        context['stu_number'] = self.stu.number
        return context


class Sua_ApplicationDelete(PermissionRequiredMixin, generic.edit.DeleteView):
    model = Sua_Application
    success_url = reverse_lazy('sua:admin-index')
    permission_required = 'sua.delete_sua_application'
    login_url = '/'


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required
def index(request):
    usr = request.user
    sua_list = []  # 公益时记录
    sa_list = []  # 公益时申请
    appeals_list = []  # 申诉记录
    gsap_list = []  # 活动记录
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
        i = 0
        for sua in stu.sua_set.filter(is_valid=True).order_by('-date'):
            i += 1
            sua_list.append((i, sua))
        i = 0
        for sua in stu.sua_set.order_by('-sua_application__date'):
            if hasattr(sua, 'sua_application'):
                i += 1
                sa_list.append((i, sua.sua_application))
        # 获取申诉列表
        i = 0
        for appeal in stu.appeal_set.order_by('-date'):
            i += 1
            appeals_list.append((i, appeal))

    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
        suahours = '-.-'
    # 组织公益时活动的公示
    gsaps = GSuaPublicity.objects.filter(
        is_published=True,
        published_begin_date__lte=timezone.now(),
        published_end_date__gt=timezone.now()
    )
    for gsap in gsaps:
        teams = dict()
        suass = gsap.gsua.suas.order_by('team', 'suahours', 'student__name')
        i = 0
        for sua in suass:
            i += 1
            if sua.team not in teams:
                teams[sua.team] = dict()
            if sua.suahours not in teams[sua.team]:
                teams[sua.team][sua.suahours] = []
            teams[sua.team][sua.suahours].append(sua.student.name)
        gsap_list.append((gsap, teams))
    return render(request, 'sua/index.html', {
        'stu_name': name,
        'stu_number': number,
        'stu_suahours': suahours,
        'sua_list': sua_list,
        'sa_list': sa_list,
        'ap_list': appeals_list,
        'gsap_list': gsap_list,
    })


@login_required
def apply_sua(request):
    usr = request.user
    stu = None
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
    date = timezone.now()
    year = date.year
    month = date.month
    if month < 9:
        year_before = year - 1
        year_after = year
    else:
        year_before = year
        year_after = year + 1

    # 表单处理
    if request.method == 'POST':
        suaForm = SuaForm(request.POST, prefix='suaForm')
        proofForm = ProofForm(request.POST, request.FILES, prefix='proofForm')
        sua_ApplicationForm = Sua_ApplicationForm(
            request.POST,
            prefix='sua_ApplicationForm',
        )
        if suaForm.is_valid() and\
                proofForm.is_valid() and\
                sua_ApplicationForm.is_valid() and\
                stu is not None:
            # 生成Models
            if proofForm.cleaned_data['is_offline']:
                offlineProofSet = Proof.objects.filter(is_offline=True)
                if offlineProofSet.count == 0:
                    assert(User.objects.filter(is_superuser=True).count != 0)
                    proof = Proof.objects.create(
                        user=User.objects.filter(is_superuser=True)[0],
                        date=date,
                        is_offline=True,
                    )
                    proof.save()
                else:
                    proof = offlineProofSet[0]
            else:
                proof = proofForm.save(commit=False)
            sua = suaForm.save(commit=False)
            sua_Application = sua_ApplicationForm.save(commit=False)
            # 处理proof
            if not proofForm.cleaned_data['is_offline']:
                proof.user = usr
                proof.date = date
                proof.save()
            # 处理sua
            sua.student = stu
            sua.last_time_suahours = 0.0
            sua.is_valid = False
            sua.save()
            # 处理sua_Application
            sua_Application.sua = sua
            sua_Application.date = date
            sua_Application.proof = proof
            sua_Application.is_checked = False
            sua_Application.save()
            return HttpResponseRedirect('/')
    else:
        suaForm = SuaForm(prefix='suaForm')
        proofForm = ProofForm(prefix='proofForm')
        sua_ApplicationForm = Sua_ApplicationForm(
            prefix='sua_ApplicationForm',
        )

    return render(request, 'sua/apply_sua.html', {
        'stu_name': name,
        'stu_number': number,
        'stu_suahours': suahours,
        'apply_date': date.date(),
        'apply_year_before': year_before,
        'apply_year_after': year_after,
        'proofForm': proofForm,
        'suaForm': suaForm,
        'sua_ApplicationForm': sua_ApplicationForm,
    })


@login_required
def appeal_for(request):
    usr = request.user
    stu = None
    gsuap = GSuaPublicity.objects.get(pk=int(request.GET.get('gsuap_id')))
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
    date = timezone.now()
    year = date.year
    month = date.month
    if month < 9:
        year_before = year - 1
        year_after = year
    else:
        year_before = year
        year_after = year + 1
    # 表单处理
    if request.method == 'POST':
        print(gsuap)
        appealForm = AppealForm(request.POST, prefix='appealForm')
        if appealForm.is_valid() and\
                stu is not None and\
                gsuap is not None:
            if date <= gsuap.published_end_date:
                # 生成Models
                appeal = appealForm.save(commit=False)
                # 处理appeal
                appeal.student = stu
                appeal.date = date
                appeal.gsua = gsuap.gsua
                appeal.is_checked = False
                appeal.feedback = ''
                appeal.save()
                return HttpResponseRedirect('/')
    else:
        print(gsuap)
        appealForm = AppealForm(prefix='appealForm')
    return render(request, 'sua/appeal_for.html', {
        'stu_name': name,
        'stu_number': number,
        'stu_suahours': suahours,
        'appealYearBefore': year_before,
        'appealYearAfter': year_after,
        'appealDate': date.date(),
        'appealForm': appealForm,
        'gsuap': gsuap,
    })


class ApplicationDetailView(generic.DetailView):
    model = Sua_Application
    template_name = 'sua/application_detail.html'
    context_object_name = 'sa'

    def get_queryset(self):
        user = self.request.user
        return Sua_Application.objects.filter(
            sua__student__user=user
        )

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        sa = self.get_object()
        usr = self.request.user
        stu = None
        suahours = 0
        if hasattr(usr, 'student'):
            stu = usr.student
            name = stu.name
            number = stu.number
            suahours = stu.suahours
        else:
            if usr.is_staff:
                name = 'Admin.' + usr.username
            else:
                name = 'NoStuInfo.' + usr.username
            number = '------'
        year = sa.date.year
        month = sa.date.month
        if month < 9:
            year_before = year - 1
            year_after = year
        else:
            year_before = year
            year_after = year + 1
        print(context)
        context['year_before'] = year_before
        context['year_after'] = year_after
        context['stu_name'] = name
        context['stu_number'] = number
        context['stu_suahours'] = suahours
        return context


@login_required
def adminIndex(request):
    usr = request.user
    if not usr.is_staff:
        return HttpResponseRedirect('/')
    else:
        students = []  # 全体学生
        gsuaps = []  # 全体活动公示
        appeals = []  # 全体申诉

        # 获取全体学生
        i = 0
        for stu in Student.objects.order_by('number'):
            i += 1
            students.append((i, stu))
        # 获取全体活动公示
        i = 0
        for gsuap in GSuaPublicity.objects.order_by('-published_begin_date'):
            i += 1
            gsuaps.append((i, gsuap))
        # 获取全体申诉
        i = 0
        for appeal in Appeal.objects.order_by('-date'):
            i += 1
            appeals.append((i, appeal))

        # 返回render
        return render(request, 'sua/admin_index.html', {
            'students': students,
            'gsuaps': gsuaps,
            'appeals': appeals,
        })
