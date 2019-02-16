from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.decorators import list_route, detail_route
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAdminUser

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, resolve


class AddFormMixin(object):
    """
    以表单的方式创建一个model实例。
    """
    add_serializer_class = None
    add_success_url = None

    def add(self, request):
        if request.method == 'GET':
            serializer = self.get_add_serializer(context={'request': request})
            return Response({'serializer': serializer})
        elif request.method == 'POST':
            # print(request.data)
            serializer = self.get_add_serializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                return Response({'serializer': serializer})
            self.perform_add(serializer)
            return self.get_add_response(serializer)

    def get_add_serializer(self, *args, **kwargs):
        return self.add_serializer_class(*args, **kwargs)

    def get_add_success_url(self, *args, **kwargs):
        return self.add_success_url

    def perform_add(self, serializer):
        serializer.save()

    def get_add_response(self, serializer):
        return HttpResponseRedirect(serializer.data['url'])


class ChangeFormMixin(object):
    """
    以表单的方式更新一个model实例。
    """
    change_serializer_class = None
    change_success_url = None

    def change(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.method == 'GET':
            serializer = self.get_change_serializer(instance, context={'request': request})
            extra_data = self.get_extra_data(serializer)
            return Response({
                'serializer': serializer,
                'extra_data': extra_data,
            })
        elif request.method == 'POST':
            serializer = self.get_change_serializer(instance=instance, data=request.data, context={'request': request})
            if not serializer.is_valid():
                serializer = self.get_change_serializer(instance, context={'request': request})
                return Response({'serializer': serializer})
            self.perform_change(serializer)
            return self.get_change_response(serializer)

    def get_change_serializer(self, *args, **kwargs):
        return self.change_serializer_class(*args, **kwargs)

    def get_change_success_url(self, *args, **kwargs):
        return self.change_success_url

    def perform_change(self, serializer):
        serializer.save()

    def get_extra_data(self, serilaizer):
        return None

    def get_change_response(self, serializer):
        return HttpResponseRedirect(serializer.data['url'])


class DetailFormMixin(object):
    """
    以Html的方式显示一个model实例。
    """
    detail_serializer_class = None

    def detail(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_detail_serializer(instance, context={'request': request})
        return self.get_detail_response(serializer)

    def get_detail_serializer(self, *args, **kwargs):
        return self.detail_serializer_class(*args, **kwargs)

    def get_detail_response(self, serializer):
        return Response({'serializer': serializer})


class DeleteFormMixin(object):
    """
    删除一个Model实例
    """
    delete_success_url = None

    @detail_route(
        methods=['get', 'delete'],
        permission_classes = (IsAdminUser, ),
    )
    def delete(self, request, *args, **kwargs):
        self.set_delete_success_url()
        instance = self.get_object()
        pk = instance.pk
        self.perform_delete(instance)
        return self.get_delete_response()

    def set_delete_success_url(self, *args, **kwargs):
        pass

    def perform_delete(self, instance):
        instance.delete()

    def get_delete_response(self):
        return HttpResponseRedirect(self.delete_success_url)
