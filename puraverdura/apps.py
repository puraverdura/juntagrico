from django.apps import AppConfig

class MyConfig(AppConfig):
    name = 'puraverdura'
    verbose_name = "My App"

    def ready(self):
        import puraverdura.signals