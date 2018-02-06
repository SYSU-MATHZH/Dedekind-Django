from django.views.generic import TemplateView


class BaseView(TemplateView):
    components = {}

    def get(self, request, *args, **kwargs):
        serializeds = self.do_serializations(request)
        context = self.get_context_data(**kwargs, **serializeds)
        return self.render_to_response(context)

    def get_components(self):
        return self.components

    def do_serializations(self, request):
        components = self.get_components()
        serializeds = {}
        for component, handler_name in components.items():
            handler = getattr(self, handler_name)
            assert component not in serializeds.keys()
            serializeds[component] = handler(request)
        return serializeds
