from rest_framework import viewsets
from django.db.models.query import QuerySet

# from rest_framework import status
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from rest_framework.renderers import TemplateHTMLRenderer

from project.sua.models import Student
from project.sua.views.form.serializers import AddStudentSerializer

import project.sua.views.utils.tools as tools

class BaseViewSet(
    viewsets.GenericViewSet,

):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None
    delete_success_url = None
    revoke_success_url = None
    revoke_queryset = None
    components = {}

    def get_components(self):
        return self.components

    def get_context(self, request, *args, **kwargs):
        # print(request.GET)
        components = self.get_components()
        extra_context = kwargs.get('extra_context', {})
        context = {}
        for component, handler_name in components.items():
            handler = getattr(self, handler_name)
            assert component not in context.keys()
            context[component] = handler(request, *args, **kwargs)
        context.update(extra_context)
        return context

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset,
            many=True
        )
        return Response(self.get_context(request, extra_context={'serializer': serializer}))

    @detail_route(methods=['get'])
    def detail(self, request, *args, **kwargs):
        from_url = '/'
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if 'from' in request.GET:
            from_url = request.GET['from']
            print(from_url)
        if 'created' in serializer.data:
            created  = tools.DateTime2String_SHOW(tools.TZString2DateTime(serializer.data['created']))
            return Response(self.get_context(request, *args, **kwargs, extra_context={'serializer': serializer, 'created':created,'from_url':from_url}))
        else:
            return Response(self.get_context(request, *args, **kwargs, extra_context={'serializer': serializer, 'from_url':from_url}))

    @list_route(methods=['get', 'post'])
    def add(self, request, *args, **kwargs):

        if request.method == 'GET':
            serializer = self.get_serializer()
            return Response(self.get_context(request, *args, **kwargs, extra_context={'serializer': serializer}))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return HttpResponseRedirect(serializer.data['url'])

    def perform_create(self, serializer):
        serializer.save()

    @detail_route(methods=['get', 'post'])
    def change(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.method == 'GET':
            serializer = self.get_serializer(instance, context={'request': request})
            extra_data = self.get_extra_data(serializer)
            return Response({
                'serializer': serializer,
                'extra_data': extra_data,
            })
            Response(self.get_context(request, *args, **kwargs, extra_context={'serializer': serializer, 'extra_data': extra_data}))

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return HttpResponseRedirect(serializer.data['url'])

    def perform_update(self, serializer):
        serializer.save()

    def get_extra_data(self, serilaizer):
        return None

    @detail_route(methods=['get'])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        deleted = None
        if user.is_staff or user.student.power == 1:
            if user.is_staff:
                deleted = user.username
            elif user.student.power == 1:
                deleted = user.student.name
        instance.deleted_by = deleted
        instance.save()
        self.perform_delete(instance)
        return self.get_delete_response()

    def perform_delete(self, instance):
        instance.delete()

    def get_delete_response(self):
        return HttpResponseRedirect(self.delete_success_url)

    def get_queryset(self):
        if self.action != 'revoke':
            return super(BaseViewSet, self).get_queryset()
        assert self.revoke_queryset is not None, (
            "'%s' should either include a `revoke_queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.revoke_queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    @detail_route(methods=['get'])
    def revoke(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_revoke(instance)
        return self.get_revoke_response()

    def perform_revoke(self, instance):
        instance.full_restore()

    def get_revoke_response(self):
        return HttpResponseRedirect(self.revoke_success_url)

class StudentViewSet(BaseViewSet):
    # template_name = 'sua/tmp/test.html'
    serializer_class = AddStudentSerializer
    queryset = Student.objects.all()

    def get_template_names(self):
        print(self.action)
        return ['sua/tmp/test.html']

    def get_context(self, request, *args, **kwargs):
        context = super(StudentViewSet, self).get_context(request, *args, **kwargs)
        print(context)
        context.update({'year': 2016})
        return context
