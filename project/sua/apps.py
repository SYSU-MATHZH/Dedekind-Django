from django.apps import AppConfig


class SuaConfig(AppConfig):
    name = 'project.sua'

    def ready(self):
        import project.sua.signals.handlers
