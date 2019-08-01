from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = "个人信息"

    def ready(self):
        import comment.signals
