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
        serializeds = self.do_serializations(request, *args, **kwargs)
        # context = self.get_context_data(**kwargs, **serializeds)
        context.update(serializeds)
        return Response(context)

    def post(self, request, *args, **kwargs):
        self.do_deserializations(self, request, *args, **kwargs)
        url = self.get_redirect_url(*args, **kwargs)
        if url:
            return HttpResponseRedirect(url)
        else:
            return HttpResponseGone()

    def get_components(self):
        return self.components

    def do_serializations(self, request, *args, **kwargs):  # 序列化请重写这个方法
        components = self.get_components()
        serializeds = {}
        for component, handler_name in components.items():
            handler = getattr(self, handler_name)
            assert component not in serializeds.keys()
            serializeds[component] = handler(request, *args, **kwargs)
        return serializeds

    def do_deserializations(self, request, *args, **kwargs):  # 反序列化请重写这个方法
        pass

    def get_redirect_url(self, *args, **kwargs):
        if self.url:
            url = self.url % kwargs
        else:
            return None
        args = self.request.META.get('QUERY_STRING', '')
        if args and self.query_string:
            url = "%s?%s" % (url, args)
        return url


# class BaseView(TemplateView):
#     components = {}
#     url = None
#
#     def get(self, request, *args, **kwargs):
#         serializeds = self.do_serializations(request, *args, **kwargs)
#         context = self.get_context_data(**kwargs, **serializeds)
#         return self.render_to_response(context)
#
#     def post(self, request, *args, **kwargs):
#         self.do_deserializations(self, request, *args, **kwargs)
#         url = self.get_redirect_url(*args, **kwargs)
#         if url:
#             return HttpResponseRedirect(url)
#         else:
#             return HttpResponseGone()
#
#     def get_components(self):
#         return self.components
#
#     def do_serializations(self, request, *args, **kwargs):  # 序列化请重写这个方法
#         components = self.get_components()
#         serializeds = {}
#         for component, handler_name in components.items():
#             handler = getattr(self, handler_name)
#             assert component not in serializeds.keys()
#             serializeds[component] = handler(request)
#         return serializeds
#
#     def do_deserializations(self, request, *args, **kwargs):  # 反序列化请重写这个方法
#         pass
#
#     def get_redirect_url(self, *args, **kwargs):
#         if self.url:
#             url = self.url % kwargs
#         else:
#             return None
#         args = self.request.META.get('QUERY_STRING', '')
#         if args and self.query_string:
#             url = "%s?%s" % (url, args)
#         return url
