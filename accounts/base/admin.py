# from mainapp.admin.sites import MainappAdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
# from simple_history.admin import SimpleHistoryAdmin
# from ..models import User, UserGroup
from django.contrib.auth import get_user_model
from ..forms import CustomUserCreationForm, CustomUserChangeForm
from django.conf import settings



CustomUser = get_user_model()



class BaseCustomGroupAdmin(GroupAdmin):
    fields = settings.USER_GROUP_CONFIG["fields"]
    list_display = settings.USER_GROUP_CONFIG["list_display"]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not settings.USER_GROUP_CONFIG["is_delete_selected_action"]:
            if "delete_selected" in actions:
                del actions["delete_selected"]
        return actions



class BaseCustomUserAdmin(UserAdmin):
    list_display = settings.USER_CONFIG["list_display"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ["tel"]}),)
    #add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ["tel"]}),)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not settings.USER_CONFIG["is_delete_selected_action"]:
            if "delete_selected" in actions:
                del actions["delete_selected"]
        return actions




