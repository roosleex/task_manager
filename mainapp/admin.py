from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import UserGroup
from accounts.admin import CustomGroupAdmin,CustomUserAdmin 
from .models import Task


CustomUser = get_user_model()
admin.site.register(UserGroup, CustomGroupAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Task)


