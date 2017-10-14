from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from sua.models import Sua, Sua_Application, Proof, Student, Appeal, SuaGroup


def get_SuaGroup_Choices():
    suaGroups = SuaGroup.objects.order_by('rank')
    suaGroup_Choices = []
    for suaGroup in suaGroups:
        suaGroup_Choices.append((suaGroup.pk, suaGroup.name))
    return suaGroup_Choices


class MyDateWidget(AdminDateWidget):
    def format_value(self, value):
        old_value = super(MyDateWidget, self).format_value(value)
        if old_value is None:
            return old_value
        dates = old_value.split('/')
        new_value = '-'.join(dates)
        return new_value


class LoginForm(forms.Form):
    user_name = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'text_box'})
    )
    user_password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'text_box'})
    )
    loginstatus = forms.BooleanField(required=False)


class StudentForm(ModelForm):
    initial_password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入新的初始密码',
    }), required=False)
    group = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
        'class': 'checkbox-inline',
    }), choices=get_SuaGroup_Choices())

    class Meta:
        model = Student

        fields = [
            'number',
            'name',
            'grade',
            'suahours',
        ]
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入学生学号（这将会作为学生的用户名）',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入学生姓名',
            }),
            'suahours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入学生当前的公益时数',
            }),
            'grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入学生年级(如2017级)',
            }),
        }


class SuaForm(ModelForm):
    class Meta:
        model = Sua
        fields = [
            'group',
            'title',
            'team',
            'date',
            'suahours',
        ]
        widgets = {
            'group': forms.Select(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入活动名称',
            }),
            'team': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'date': MyDateWidget(attrs={
                'class': 'form-control',
            }),
            'suahours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入公益时数',
            }),

        }


class ProofForm(ModelForm):
    class Meta:
        model = Proof
        fields = [
            'is_offline',
            'proof_file',
        ]
        widgets = {
        }


class Sua_ApplicationForm(ModelForm):
    class Meta:
        model = Sua_Application
        fields = [
            'detail',
            'contact',
        ]
        widgets = {
            'detail': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入活动详情',
                'cols': 20,
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入联系方式',
            })
        }


class AppealForm(ModelForm):
    class Meta:
        model = Appeal
        fields = [
            'claim',
        ]
        widgets = {
            'claim': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入申诉内容',
                'cols': 20,
            }),
        }
