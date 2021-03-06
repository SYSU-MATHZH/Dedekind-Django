from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponseGone

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None
    url = None
    components = {}

    def get(self, request, *args, **kwargs):
        context = {}
        serialized = self.serialize(request, *args, **kwargs)
        # context = self.get_context_data(**kwargs, **serializeds)
        context.update(serialized)
        return Response(context)

    def post(self, request, *args, **kwargs):
        if self.deserialize(request, *args, **kwargs):
            url = self.get_redirect_url(*args, **kwargs)
            if url:
                return HttpResponseRedirect(url)
            else:
                return HttpResponseGone()
        else:
            return self.get(request, *args, **kwargs)

    def get_components(self):
        return self.components

    def serialize(self, request, *args, **kwargs):  # 序列化及其他业务逻辑请重写这个方法
        components = self.get_components()
        serialized = {}
        for component, handler_name in components.items():
            handler = getattr(self, handler_name)
            assert component not in serialized.keys()
            serialized[component] = handler(request, *args, **kwargs)
        return serialized

    def deserialize(self, request, *args, **kwargs):  # 反序列化请重写这个方法
        return True

    def get_redirect_url(self, *args, **kwargs):
        if self.url:
            url = self.url % kwargs
        else:
            return None
        args = self.request.META.get('QUERY_STRING', '')
        if args:
            url = "%s?%s" % (url, args)
        return url
