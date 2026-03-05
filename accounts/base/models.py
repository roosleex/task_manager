from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from common.model_utils import get_tel_number_validator



class BaseUser(AbstractUser):
    tel = models.CharField(verbose_name="Номер телефону", max_length=15, validators=get_tel_number_validator())

    def __str__(self):
        return self.username

    class Meta:
        abstract = True
        db_table = 'auth_user'
        verbose_name = "користувач"
        verbose_name_plural = "користувачі"
        ordering = ["-id"]
        


class BaseUserGroup(Group):
    description = models.CharField(verbose_name="Опис", max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        verbose_name = "група"
        verbose_name_plural = "групи"
        ordering = ["-id"]



        
