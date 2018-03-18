from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.utils import timezone
from project.sua.storage import FileStorage
import datetime
import hashlib
from .token import TOKEN


YEAR_CHOICES = []
for r in range(2016, datetime.datetime.now().year):
    YEAR_CHOICES.append((r, r))

EXPIRE_TIME = 86400


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    number = models.IntegerField(_("Student Number"))
    suahours = models.FloatField(default=0)
    name = models.CharField(max_length=100)
    classtype = models.CharField(max_length=100)
    grade = models.IntegerField(
        _("Student Grade"),
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year
    )
    phone = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name


class SuaGroup(models.Model):
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    contact = models.CharField(max_length=100, blank=True)
    rank = models.IntegerField(blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        related_name='activities',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField('创建日期', auto_now_add=True)
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=400)
    group = models.CharField(max_length=100)
    date = models.DateTimeField('活动日期')
    is_valid = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title


class Sua(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        related_name='suas',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        Student,
        related_name='suas',
        on_delete=models.CASCADE,
    )
    activity = models.ForeignKey(
        Activity,
        related_name='suas',
        on_delete=models.CASCADE,
    )
    team = models.CharField(max_length=100)
    suahours = models.FloatField()
    added = models.FloatField(default=0.0)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.student.name + '的 ' + self.activity.title

    def clean_suahours(self):
        self.student.suahours -= self.added
        self.student.save()
        self.added = 0.0

    def update_student_suahours(self):
        if self.added != self.suahours:
            self.clean_suahours()
            self.student.suahours += self.suahours
            self.student.save()
            self.added = self.suahours


class Proof(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='proofs',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    is_offline = models.BooleanField(default=False)
    proof_file = models.FileField(
        upload_to='proofs',
        storage=FileStorage(),
        blank=True,
    )

    def __str__(self):
        if self.is_offline:
            return '线下证明'
        else:
            return self.owner.username +\
                '_' +\
                self.created.strftime("%Y%m%d%H%M%S")


class Application(models.Model):
    sua = models.OneToOneField(
        Sua,
        related_name='application',
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        'auth.User',
        related_name='applications',
        on_delete=models.CASCADE,
    ) 
    created = models.DateTimeField('创建日期', auto_now_add=True)
    contact = models.CharField(max_length=100, blank=True)
    proof = models.ForeignKey(
        Proof,
        related_name='applications',
        on_delete=models.CASCADE,
    )
    is_checked = models.BooleanField(default=False)
    status = models.IntegerField(default=0)  # 0: 通过; 1: 未通过; 2: 需要线下证明
    feedback = models.CharField(max_length=400, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.sua.student.name + '的 ' + self.sua.activity.title + '的 ' + '申请'


class Publicity(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        related_name='publicities',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField('创建日期', auto_now_add=True)
    activity = models.ForeignKey(
        Activity,
        related_name='publicities',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=400)
    contact = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    begin = models.DateTimeField('开始公示时间', default=timezone.now)
    end = models.DateTimeField('结束公示时间')
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.title


class Appeal(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        related_name='appeals',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField('创建日期', auto_now_add=True)
    student = models.ForeignKey(
        Student,
        related_name='appeals',
        on_delete=models.CASCADE,
    )
    publicity = models.ForeignKey(
        Publicity,
        related_name='appeals',
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=400, blank=True)
    status = models.IntegerField(default=0)  # 0: 通过; 1: 未通过; 2: 需要线下处理
    is_checked = models.BooleanField(default=False)
    feedback = models.CharField(max_length=400, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return '对' + str(self.publicity) + '的申诉'


class Nonce(models.Model):
    nonce = models.IntegerField()
    timestamp = models.IntegerField()

    def getSignature(self):
        s = bytes(str(self.nonce) + str(self.timestamp) + TOKEN, encoding='utf8')
        signature = hashlib.sha1(s).hexdigest()
        return signature
