from django.apps import AppConfig
from django.conf import settings


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = settings.COMMON_CONFIG["accounts_config_verbose_name"]
    verbose_name_plural = settings.COMMON_CONFIG["accounts_config_verbose_name_plural"]




