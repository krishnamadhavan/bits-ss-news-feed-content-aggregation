from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "news_feed_content.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import news_feed_content.users.signals  # noqa F401
        except ImportError:
            pass
