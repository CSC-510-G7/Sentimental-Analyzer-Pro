from django.apps import AppConfig


class RealworldConfig(AppConfig):
    name = 'realworld'

    def ready(self):
        # import realworld.signals
        return
