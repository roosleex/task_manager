from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm



class BaseCustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )



class BaseCustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )



