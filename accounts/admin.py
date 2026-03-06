# from mainapp.admin.sites import MainappAdminSite
from .base.admin import BaseCustomGroupAdmin, BaseCustomUserAdmin
# from simple_history.admin import SimpleHistoryAdmin
# from .models import User, UserGroup
# from django.contrib.auth import get_user_model
# from django.conf import settings



class CustomGroupAdmin(BaseCustomGroupAdmin):
    pass



class CustomUserAdmin(BaseCustomUserAdmin):
    pass
