from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.utils import timezone
from project.sua.storage import FileStorage
import datetime
import hashlib


YEAR_CHOICES = []
for r in range(2016, datetime.datetime.now().year):
    YEAR_CHOICES.append((r, r))

EXPIRE_TIME = 86400

"""
实现软删除(需要继承该类)
通过deletedAt字段保存删除的时间。
若记录没有被删除，那么设置该值为None，如果被删除，那么设置时间为删除的时间。
注意：在取得元素的时候，需要使用User.objects.filter(deletedAt=None)，而不是all()
"""
class BaseSchema(models.Model):
    deletedAt = models.DateTimeField("删除时间", null=True, default=None, blank=True)

    class Meta:
        abstract = True     #设为抽象基类，否则会出现id字段冲突的情况

    def delete(self, using=None, keep_parents=False):
        self.deletedAt = timezone.now()
        self.save()


class Student(BaseSchema):
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
    power = models.IntegerField(default=0)  # 0:普通学生  1:活动级管理员

    def __str__(self):
        return self.name

    def totalhours(self):
        total = 0
        for sua in self.suas.filter(deletedAt=None, is_valid=True, activity__is_valid=True):
                total += sua.suahours
        self.suahours = total
        self.save()
        return total

    def get_suas(self):
        return self.suas.filter(deletedAt=None, is_valid=True, activity__is_valid=True)


class SuaGroup(BaseSchema):
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


class Activity(BaseSchema):
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
    iscreatebystudent = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_suas(self):
        return self.suas.filter(deletedAt=None, is_valid=True)

    def get_suas_all(self):
        return self.suas.filter(deletedAt=None)

    def delete(self, using=None, keep_parents=False):
        self.deletedAt = timezone.now()
        self.is_valid = False
        self.save()

class Sua(BaseSchema):
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
    suahours = models.FloatField(default=0.0)
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

    def delete(self, using=None, keep_parents=False):
        self.deletedAt = timezone.now()
        self.is_valid = False
        self.save()


class Proof(BaseSchema):
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


class Application(BaseSchema):
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


class Publicity(BaseSchema):
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


class Appeal(BaseSchema):
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
        TOKEN = "test"
        s = bytes(str(self.nonce) + str(self.timestamp) + TOKEN, encoding='utf8')
        signature = hashlib.sha1(s).hexdigest()
        return signature
