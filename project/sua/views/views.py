from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from project.sua.forms import LoginForm
from project.sua.serializers import StudentSerializer, UserSerializer, PublicitySerializer, SuaSerializer, ApplicationSerializer
from project.sua.models import Publicity, Sua, Application


@login_required
def index(request):
    # load user
    user = request.user
    student = None
    if hasattr(user, 'student'):
        student = user.student
    userSerializer = UserSerializer(user, context={'request': request})
    studentSerializer = StudentSerializer(student, context={'request': request})

    # load publicities
    publicities = Publicity.objects.filter(
        is_published=True,
        begin__lte=timezone.now(),
        end__gte=timezone.now()
    )
    publicitySerializer = PublicitySerializer(publicities, many=True, context={'request': request})

    # load suas
    suaSerializer = SuaSerializer(student.suas, many=True, context={'request': request})

    # load applications


    return render(request, 'sua/index.html', {
        'user': userSerializer.data,
        'student': studentSerializer.data,
        'suas': suaSerializer.data,
        'applications': userSerializer.data['applications'],
        'appeals': studentSerializer.data['appeals'],
        'publicities': publicitySerializer.data,
    })


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
